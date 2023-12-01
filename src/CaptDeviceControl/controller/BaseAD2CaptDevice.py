import logging
import os
import sys
import time
from abc import abstractmethod
from collections import deque

from PySide6.QtCore import QObject, QThreadPool
from numpy import ndarray
from rich.logging import RichHandler


from CaptDeviceControl.model.AD2CaptDeviceModel import AD2CaptDeviceModel, AD2CaptDeviceSignals
from CaptDeviceControl.model.AD2Constants import AD2Constants
from multiprocessing import Process, Queue, Value, Lock

from CaptDeviceControl.controller.mp_AD2Capture.MPCaptDeviceControl import MPCaptDeviceControl


class BaseAD2CaptDevice(QObject):

    def __init__(self, ad2capt_model: AD2CaptDeviceModel, start_capture_flag: Value):
        super().__init__()
        self.model = ad2capt_model

        self.pref = "AD2CaptDev"

        self.handler = RichHandler(rich_tracebacks=True)
        self.logger = logging.getLogger(f"AD2Controller({os.getpid()})")
        self.logger.handlers = [self.handler]
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s %(message)s')
        self.handler.setFormatter(formatter)


        self.signals = AD2CaptDeviceSignals()

        self.thread_manager = QThreadPool()
        self.kill_thread = False
        # self.thread_manager.setMaxThreadCount(3)
        # self.thread_manager.se
        # self.thread_manager.setThreadPriority(QThread.HighestPriority)

        self.lock = Lock()
        #self.proc = None
        self.stream_data_queue = Queue()
        self.capture_data_queue = Queue()
        #self.state_queue = Queue()

        if start_capture_flag is None:
            self.start_capture_flag = Value('i', 0, lock=self.lock)
        else:
            self.start_capture_flag = start_capture_flag
        self.kill_capture_flag = Value('i', 0, lock=self.lock)
        #self.end_process_flag = Value('i', False, lock=self.lock)

        # Number of sa
        self.streaming_data_dqueue: deque = None # a dqueue, initialize later

        self.status_dqueue = deque(maxlen=int(1))
        self.unconsumed_capture_data = 0

        self.mpcaptdevicecontrol = MPCaptDeviceControl(self.model,
                                                       self.stream_data_queue,
                                                       self.capture_data_queue,
                                                       self.start_capture_flag,
                                                       self.kill_capture_flag,
                                                       enable_internal_logging=False)

        #self.mpcaptdevicecontrol.discover_connected_devices_finished.connect(
        #    lambda x: type(self.model).connected_devices.fset(self.model, x))


        #self.mpcaptdevicecontrol.connected_devices()

    def device_selected_index_changed(self):
        print(self.model.device_information.device_index)
        self.mpcaptdevicecontrol.ain_channels(self.model.device_information.device_index)
        #self.mpcaptdevicecontrol
    def connect_device(self, device_id):
        self.mpcaptdevicecontrol.open_device(device_id)
        self.mpcaptdevicecontrol.start_capture(
            self.model.sample_rate,
            self.model.device_information.device_index)
        self.start_device_process()
        return True

    def close_device(self):
        self.mpcaptdevicecontrol.close_device()


    def discover_connected_devices(self):
        self.mpcaptdevicecontrol.connected_devices()

    @abstractmethod
    def update_device_information(self):
        raise NotImplementedError

    @abstractmethod
    def _capture(self):
        raise NotImplementedError

    def set_ad2_acq_status(self, record):
        if record:
            self.model.start_recording = True
            self.model.stop_recording = False
            self.logger.info(f"[{self.pref} Task] >>>>>>>>>> Started acquisition!")

        elif record == False:
            self.model.start_recording = False
            self.model.stop_recording = True
            self.logger.info(f"[{self.pref} Task] >>>>>>>>>>> Stopped acquisition!")

        else:
            self.model.start_recording = False
            self.model.stop_recording = False
            self.logger.info(f"[{self.pref} Task] >>>>>>>>>>> Reset acquisition!")

    def _init_device_parameters(self):
        pass
        #sample_rate = int(self.model.ad2captdev_config.get_sample_rate())
        #total_samples = int(self.model.ad2captdev_config.get_total_samples())
        #channel = 0  # TODO Read channel from input

        #self.model.sample_rate = int(sample_rate)
        #self.model.n_samples = int(total_samples)
        #self.model.selected_ain_channel = int(channel)
        #self.logger.info(f"AD2 device initialized {self.model.selected_ain_channel} with "
        #                 f"acquisition rate {self.model.sample_rate} Hz and "
        #                 f"samples {self.model.n_samples}")

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def clear_data(self):
        self.model.recorded_samples = []
        self.model.recorded_sample_stream = []

    def start_capture(self, clear=True):
        print(f"Start capture. Clear {clear}")
        self.start_capture_flag.value = 1
        if clear:
            self.model.recorded_samples = []
            self.model.recorded_sample_stream = []
        self.model.start_recording = True
        self.model.stop_recording = False
        self.model.device_capturing_state = AD2Constants.CapturingState.RUNNING()

    def stop_capture(self):
        print("Stop capture")
        self.start_capture_flag.value = 0
        self.model.start_recording = False

        if self.model.reset_recording:
            self.model.device_capturing_state = AD2Constants.CapturingState.STOPPED()
            self.model.stop_recording = True
        else:
            self.model.device_capturing_state = AD2Constants.CapturingState.PAUSED()

    def capture(self, start, clear=True):
        if start:
            self.start_capture(clear)
        else:
            self.stop_capture()

    def reset_capture(self):
        self.logger.info("Resetting captured samples for new measurement.")
        self.model.recorded_samples = []
        self.model.measurement_time = 0
        self.model.capturing_finished = False

    # ==================================================================================================================
    def start_device_process(self):
        self.logger.info(f"[{self.pref} Task] Starting capturing process...")
        #self.logger.debug(f"Dataqueue maxlen={int(self.model.duration_streaming_history * self.model.sample_rate)}")
        self.streaming_data_dqueue = deque(maxlen=int(self.model.duration_streaming_history * self.model.sample_rate))
        #print(self.model.duration_streaming_history * self.model.sample_rate)
        self.stream_data_queue.maxsize = int(self.model.duration_streaming_history * self.model.sample_rate)
        #self.proc = Process(target=mp_capture,
        #               args=(
        #                   self.stream_data_queue, self.capture_data_queue, self.state_queue,
        #                   self.start_capture_flag, self.end_process_flag,
        #                   device_id, self.model.selected_ain_channel, self.model.sample_rate)
        #               )
        #self.proc.start()

        # self.thread_manager.moveToThread(())
        self.thread_manager.start(self.qt_consume_data)
        self.thread_manager.start(self.qt_stream_data)
        #self.thread_manager.start(self.qt_get_state)
    
    def qt_consume_data(self):
        while True:
            try:
                capt_data = self.capture_data_queue.get()
                if isinstance(capt_data, ndarray):
                    print(f"Capt data queue size {self.capture_data_queue.qsize()}")
                    # for d in stream_data:
                         # self.model.recorded_samples.append(d)
            except Exception as e:
                self.logger.info(f"Error while consuming data {e}")
        self.logger.info("Capture Data consume thread ended")

    def qt_stream_data(self):
        while True:
            t = time.time()
            try:
                stream_data = self.stream_data_queue.get(block=True)
                if isinstance(stream_data, ndarray):
                    #print(f"Stream data queue size {self.stream_data_queue.qsize()}")
                    for d in stream_data:
                        self.streaming_data_dqueue.append(d)
                t_end = time.time()
                #print(f"Time to get data {t_end-t}")
            except Exception as e:
                self.logger.info(f"Timeout reached. No data in queue {self.stream_data_queue.qsize()} or"
                                 f"{e}")
        self.logger.info("Streaming data consume thread ended")

    def qt_get_state(self):
        while not self.kill_thread and not bool(self.end_process_flag.value):
            while self.state_queue.qsize() > 0:
                self._set_ad2state_from_process(self.state_queue.get())
            #time.sleep(0.1)
        self.logger.info("Status data consume thread ended")

    # ==================================================================================================================
    # Destructor
    # ==================================================================================================================
    def exit(self):
       self.mpcaptdevicecontrol.safe_exit()


        