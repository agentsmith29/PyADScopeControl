import logging
import time
from abc import abstractmethod
from collections import deque

from PySide6.QtCore import QObject, QThreadPool

from CaptDeviceControl.controller.mp_AD2Capture.AD2StateMPSetter import AD2State
from CaptDeviceControl.controller.mp_AD2Capture.MPDeviceControl import mp_capture
from CaptDeviceControl.model.AD2CaptDeviceModel import AD2CaptDeviceModel, AD2CaptDeviceSignals
from CaptDeviceControl.model.AD2Constants import AD2Constants
from multiprocessing import Process, Queue, Value, Lock


class BaseAD2CaptDevice(QObject):

    def __init__(self, ad2capt_model: AD2CaptDeviceModel):
        super().__init__()
        self.model = ad2capt_model

        self.pref = "AD2CaptDev"
        self.logger = logging.getLogger(f"AD2 Device")

        self.signals = AD2CaptDeviceSignals()

        self.thread_manager = QThreadPool()
        self.kill_thread = False
        # self.thread_manager.setMaxThreadCount(3)
        # self.thread_manager.se
        # self.thread_manager.setThreadPriority(QThread.HighestPriority)

        self.lock = Lock()
        self.proc = None
        self.stream_data_queue = Queue()
        self.capture_data_queue = Queue()
        self.state_queue = Queue()

        self.start_capture_flag = Value('i', 0, lock=self.lock)
        self.end_process_flag = Value('i', False, lock=self.lock)

        # Number of sa
        self.streaming_data_dqueue: deque = None # a dqueue, initialize later

        self.status_dqueue = deque(maxlen=int(1))
        self.unconsumed_capture_data = 0


        self.discover_connected_devices()

    @abstractmethod
    def connect_device(self, device_id):
        raise NotImplementedError

    @abstractmethod
    def discover_connected_devices(self):
        raise NotImplementedError

    @abstractmethod
    def update_device_information(self):
        raise NotImplementedError

    @abstractmethod
    def _capture(self):
        raise NotImplementedError

    @abstractmethod
    def close_device(self):
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
    def start_device_process(self, device_id):
        self.logger.info(f"[{self.pref} Task] Starting capturing process...")
        #self.logger.debug(f"Dataqueue maxlen={int(self.model.duration_streaming_history * self.model.sample_rate)}")
        self.streaming_data_dqueue = deque(maxlen=int(self.model.duration_streaming_history * self.model.sample_rate))
        #print(self.model.duration_streaming_history * self.model.sample_rate)
        self.stream_data_queue.maxsize = int(self.model.duration_streaming_history * self.model.sample_rate)
        self.proc = Process(target=mp_capture,
                       args=(
                           self.stream_data_queue, self.capture_data_queue, self.state_queue,
                           self.start_capture_flag, self.end_process_flag,
                           device_id, self.model.selected_ain_channel, self.model.sample_rate)
                       )
        self.proc.start()

        # self.thread_manager.moveToThread(())
        self.thread_manager.start(self.qt_consume_data)
        self.thread_manager.start(self.qt_stream_data)
        self.thread_manager.start(self.qt_get_state)
    
    def qt_consume_data(self):
        """Consume data from the queue and plot it. This is a QThread."""
        while not self.kill_thread and not bool(self.end_process_flag.value):
            while self.capture_data_queue.qsize() > 0:
                self.model.unconsumed_capture_data = self.capture_data_queue.qsize()
                d, s = self.capture_data_queue.get()
                [self.model.recorded_samples.append(e) for e in d]
                # self.model.samples_captured = len(self.model.recorded_samples)
                self.status_dqueue.append(s)
            #time.sleep(0.01)
        self.logger.info("Capture Data consume thread ended")

    def qt_stream_data(self):
        nth_cnt = 1
        nth = 2
        while not self.kill_thread and not bool(self.end_process_flag.value):
            while self.stream_data_queue.qsize() > 0:
                self.model.unconsumed_stream_samples = self.stream_data_queue.qsize()
                for d in self.stream_data_queue.get()[0]:
                    #if nth_cnt == nth:
                    self.streaming_data_dqueue.append(d)
                    #    nth_cnt = 0
                    #nth_cnt += 1
            #time.sleep(0.01)
        self.logger.info("Streaming data consume thread ended")

    def qt_get_state(self):
        while not self.kill_thread and not bool(self.end_process_flag.value):
            while self.state_queue.qsize() > 0:
                self._set_ad2state_from_process(self.state_queue.get())
            #time.sleep(0.1)
        self.logger.info("Status data consume thread ended")

    def _set_ad2state_from_process(self, ad2state: AD2State):
        # print(ad2state.__dict__)
        self.model.pid = ad2state.pid

        self.model.dwf_version = ad2state.dwf_version

        self.model.connected = ad2state.connected
        self.model.device_name = ad2state.device_name
        self.model.device_serial_number = ad2state.device_serial_number
        self.model.device_index = ad2state.device_index

        if ad2state.acquisition_state == AD2Constants.CapturingState.RUNNING():
            self.logger.info("[START ACQ] Started acquisition")
            self.model.capturing_finished = False
            self.model.start_recording = True
            self.model.stop_recording = False
        elif ad2state.acquisition_state == AD2Constants.CapturingState.STOPPED():
            if self.model.start_recording:
                self.model.capturing_finished = True
                self.logger.info(f"[STOP ACQ] Finished acquisition {self.model.capturing_finished}.")
                # Emit a signal,  that the Capturing has finished
            self.model.start_recording = False
            self.model.stop_recording = True
        self.model.device_capturing_state = ad2state.acquisition_state

        self.model.sample_rate = ad2state.sample_rate
        self.model.selected_ain_channel = ad2state.selected_ain_channel

        self.model.ain_channels = ad2state.ain_channels
        self.model.ain_buffer_size = ad2state.ain_buffer_size
        self.model.ain_bits = ad2state.ain_bits
        self.model.ain_device_state = ad2state.ain_device_state

        self.model.recording_time = ad2state.recording_time

    # ==================================================================================================================
    # Destructor
    # ==================================================================================================================
    def stop_process(self):
        self.end_process_flag.value = True
            
        time_start = time.time()
        while self.proc.is_alive():
            time.sleep(0.1)
        self.logger.warning(f"AD2 process exited after {time.time()-time_start}s")
        self.kill_thread = True    

    def __del__(self):
        self.logger.info("Exiting AD2 controller")
        self.stop_process()
        self.logger.warning("AD2 controller exited")

        