import logging
import os
import sys
import time
from abc import abstractmethod
from collections import deque

import cmp
from PySide6.QtCore import QObject, QThreadPool, Signal

from numpy import ndarray
from rich.logging import RichHandler

from CaptDeviceControl.model.AD2CaptDeviceModel import AD2CaptDeviceModel, AD2CaptDeviceSignals
from CaptDeviceControl.model.AD2Constants import AD2Constants
from multiprocessing import Process, Queue, Value, Lock

from CaptDeviceControl.controller.mp_AD2Capture.MPCaptDeviceControl import MPCaptDeviceControl
from CaptDeviceControl.controller.mp_AD2Capture.MPCaptDevice import MPCaptDevice


class BaseAD2CaptDevice(cmp.CProcessControl):
    dwf_version_changed = Signal(str, name="dwf_version_changed")
    discovered_devices_changed = Signal(list, name="discovered_devices_changed")

    selected_device_index_changed = Signal(int, name="selected_device_index_changed")
    device_connected_changed = Signal(bool, name="connected_changed")
    device_name_changed = Signal(str, name="device_name_changed")
    device_serial_number_changed = Signal(str, name="device_serial_number_changed")

    ain_channels_changed = Signal(list, name="ain_channels_changed")
    ain_buffer_size_changed = Signal(int, name="ain_buffer_size_changed")
    analog_in_bits_changed = Signal(int, name="analog_in_bits_changed")
    analog_in_buffer_size_changed = Signal(int, name="analog_in_buffer_size_changed")
    analog_in_channel_range_changed = Signal(tuple, name="analog_in_channel_range_changed")
    analog_in_offset_changed = Signal(tuple, name="analog_in_offset_changed")

    open_device_finished = Signal(int, name="open_device_finished")
    close_device_finished = Signal(name="close_device_finished")

    device_state_changed = Signal(AD2Constants.DeviceState, name="device_state_changed")

    capture_process_state_changed = Signal(AD2Constants.CapturingState, name="capture_process_state_changed")

    def __init__(self, ad2capt_model: AD2CaptDeviceModel, start_capture_flag: Value):
        super().__init__(
            internal_log=True,
            internal_log_level=logging.DEBUG)

        self.model = ad2capt_model

        self.pref = "AD2CaptDev"

        self.thread_manager = QThreadPool()
        self.kill_thread = False

        self.lock = Lock()
        self.stream_data_queue = Queue()
        self.capture_data_queue = Queue()

        if start_capture_flag is None:
            self.start_capture_flag = Value('i', 0, lock=self.lock)
        else:
            self.start_capture_flag = start_capture_flag
        self.kill_capture_flag = Value('i', 0, lock=self.lock)

        # Number of sa
        self.streaming_dqueue: deque = None  # a dqueue, initialize later

        self.register_child_process(
            MPCaptDevice,
            self.stream_data_queue,
            self.capture_data_queue,
            self.start_capture_flag,
            self.kill_capture_flag
        )
        self.connect_signals()
        self._connect_config_signals()

    def connect_signals(self):
        self.dwf_version_changed.connect(self._on_dwf_version_changed)
        self.discovered_devices_changed.connect(self.on_discovered_devices_changed)

        self.selected_device_index_changed.connect(self.on_selected_device_index_changed)

        self.device_connected_changed.connect(
            lambda x: type(self.model.device_information).device_connected.fset(self.model.device_information, x))
        self.device_name_changed.connect(
            lambda x: type(self.model.device_information).device_name.fset(self.model.device_information, x))
        self.device_serial_number_changed.connect(
            lambda x: type(self.model.device_information).device_serial_number.fset(self.model.device_information, x))

        self.ain_channels_changed.connect(
            lambda x: type(self.model.analog_in).ain_channels.fset(self.model.analog_in, x))
        self.ain_buffer_size_changed.connect(
            lambda x: type(self.model.analog_in).ain_buffer_size.fset(self.model.analog_in, x))
        self.analog_in_bits_changed.connect(
            lambda x: type(self.model.analog_in).ain_bits.fset(self.model.analog_in, x))
        self.analog_in_buffer_size_changed.connect(
            lambda x: type(self.model.analog_in).ain_buffer_size.fset(self.model.analog_in, x))
        self.analog_in_channel_range_changed.connect(
            lambda x: type(self.model.analog_in).ai.fset(self.model.analog_in, x))
        self.analog_in_offset_changed.connect(
            lambda x: type(self.model.analog_in).ain_offset.fset(self.model.analog_in, x))

        self.device_state_changed.connect(
            lambda x: type(self.model.device_information).device_state.fset(self.model.device_information, x))
        self.capture_process_state_changed.connect(
            lambda x: type(self.model.capturing_information).device_capturing_state.fset(self.model.capturing_information, x))


        self.open_device_finished.connect(self.on_open_device_finished)

    def _connect_config_signals(self):
        self.model.ad2captdev_config.streaming_history.connect(self._on_streaming_history_changed)
    # ==================================================================================================================
    #   Device control
    # ==================================================================================================================
    @cmp.CProcessControl.register_function(open_device_finished)
    def open_device(self, device_index):
        """
        Opens the device with the given id.
        :param device_id:
        :return:
        """

    def on_open_device_finished(self, device_handle: int):
        self.logger.info(f"Opening device finished with handle {device_handle}")

    def close_device(self):
        pass
        # self.close_device()

    @cmp.CProcessControl.register_function(capture_process_state_changed)
    def start_capturing_process(self, sample_rate: float, ain_channel: int):
        """
        Starts the capturing process.
        :param sample_rate:
        :param ain_channel:
        :return:
        """
        self.streaming_dqueue = deque(maxlen=self.model.capturing_information.streaming_deque_length)
        self.thread_manager.start(self.qt_consume_data)
        self.thread_manager.start(self.qt_stream_data)

    def _on_streaming_history_changed(self, history: float):
        self.streaming_dqueue = deque(maxlen=self.model.capturing_information.streaming_deque_length)

    # ==================================================================================================================
    # DWF Version
    # ==================================================================================================================
    def _on_dwf_version_changed(self, version):
        self.model.dwf_version = version

    # ==================================================================================================================
    #   Discover connected devices
    # ==================================================================================================================
    @cmp.CProcessControl.register_function(discovered_devices_changed)
    def discover_connected_devices(self):
        """
            Discover connected devices and update the model.
            :return:
        """

    def on_discovered_devices_changed(self, devices: list):
        self.model.device_information.connected_devices = devices

    # ==================================================================================================================
    # Selected device index
    # ==================================================================================================================
    @cmp.CProcessControl.register_function(discovered_devices_changed)
    def selected_device_index(self, index):
        """
        Sets the selected device index.
        :param index: The index of the device.
        """

    def on_selected_device_index_changed(self, index):
        self.model.device_information.selected_device_index = index

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
        # sample_rate = int(self.model.ad2captdev_config.get_sample_rate())
        # total_samples = int(self.model.ad2captdev_config.get_total_samples())
        # channel = 0  # TODO Read channel from input

        # self.model.sample_rate = int(sample_rate)
        # self.model.n_samples = int(total_samples)
        # self.model.selected_ain_channel = int(channel)
        # self.logger.info(f"AD2 device initialized {self.model.selected_ain_channel} with "
        #                 f"acquisition rate {self.model.sample_rate} Hz and "
        #                 f"samples {self.model.n_samples}")

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def clear_data(self):
        self.model.recorded_samples = []
        self.model.recorded_sample_stream = []

    # def start_capture(self, clear=True):
    #    print(f"Start capture. Clear {clear}")
    #    self.start_capture_flag.value = 1
    #    if clear:
    #        self.model.recorded_samples = []
    #        self.model.recorded_sample_stream = []
    #    self.model.start_recording = True
    #    self.model.stop_recording = False
    # self.model.device_capturing_state = AD2Constants.CapturingState.RUNNING()

    def stop_capture(self):
        self.start_capture_flag.value = 0

    def start_capture(self, clear=True):
        self.start_capture_flag.value = 1

    def reset_capture(self):
        self.logger.info(f"[{self.pref} Task] Resetting capture...")
        if self.model.capturing_information.device_capturing_state == AD2Constants.CapturingState.RUNNING():
            self.stop_capture()
            self.model.capturing_information.recorded_samples = []
            self.start_capture()
        else:
            self.stop_capture()
            self.model.capturing_information.recorded_samples = []
        self.model.measurement_time = 0



    # ==================================================================================================================
    def start_device_process(self):
        self.logger.info(f"[{self.pref} Task] Starting capturing process...")
        # self.logger.debug(f"Dataqueue maxlen={int(self.model.duration_streaming_history * self.model.sample_rate)}")

        # self.proc = Process(target=mp_capture,
        #               args=(
        #                   self.stream_data_queue, self.capture_data_queue, self.state_queue,
        #                   self.start_capture_flag, self.end_process_flag,
        #                   device_id, self.model.selected_ain_channel, self.model.sample_rate)
        #               )
        # self.proc.start()

        # self.thread_manager.moveToThread(())

        # self.thread_manager.start(self.qt_get_state)

    def qt_consume_data(self):
        while True:
            t = time.time()
            try:
                capture_data = self.capture_data_queue.get(block=True)
                if isinstance(capture_data, ndarray):
                    # print(f"Stream data queue size {len(stream_data)}")
                    for d in capture_data:
                        self.model.capturing_information.recorded_samples.append(d)
                t_end = time.time()
                # print(f"Time to get data {t_end-t}")
            except Exception as e:
                self.logger.info(f"Timeout reached. No data in queue {self.stream_data_queue.qsize()} or"
                                 f"{e}")
        self.logger.info("Streaming data consume thread ended")

    def qt_stream_data(self):
        while True:
            t = time.time()
            try:
                stream_data = self.stream_data_queue.get(block=True)
                if isinstance(stream_data, ndarray):
                    # print(f"Stream data queue size {len(stream_data)}")
                    for d in stream_data:
                        self.streaming_dqueue.append(d)
                t_end = time.time()
                # print(f"Time to get data {t_end-t}")
            except Exception as e:
                self.logger.info(f"Timeout reached. No data in queue {self.stream_data_queue.qsize()} or"
                                 f"{e}")
        self.logger.info("Streaming data consume thread ended")

    def qt_get_state(self):
        while not self.kill_thread and not bool(self.end_process_flag.value):
            while self.state_queue.qsize() > 0:
                self._set_ad2state_from_process(self.state_queue.get())
            # time.sleep(0.1)
        self.logger.info("Status data consume thread ended")

    # ==================================================================================================================
    # Destructor
    # ==================================================================================================================
    def exit(self):
        self.mpcaptdevicecontrol.safe_exit()
