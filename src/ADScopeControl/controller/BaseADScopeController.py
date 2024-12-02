import logging
import math
import time
from abc import abstractmethod
from collections import deque
from multiprocessing import Queue, Value, Lock

import mpPy6
import pandas as pd
from PySide6.QtCore import QThreadPool, Signal
from PySide6.QtWidgets import QMessageBox
from numpy import ndarray

from ADScopeControl.controller.mp_AD2Capture.MPCaptDevice import MPCaptDevice
from ADScopeControl.controller.sweepHelpers import ramp
from ADScopeControl.model.AD2ScopeModel import AD2ScopeModel
from ADScopeControl.model.AD2Constants import AD2Constants


class BaseADScopeController(mpPy6.CProcessControl):
    dwf_version_changed = Signal(str, name="dwf_version_changed")
    discovered_devices_changed = Signal(list, name="discovered_devices_changed")

    selected_device_index_changed = Signal(int, name="selected_device_index_changed")
    device_connected_changed = Signal(bool, name="connected_changed")
    device_name_changed = Signal(str, name="device_name_changed")
    device_serial_number_changed = Signal(str, name="device_serial_number_changed")

    ain_channels_changed = Signal(list, name="ain_channels_changed")
    selected_ain_channel_changed = Signal(int, name="selected_ain_channel_changed")
    sample_rate_changed = Signal(float, name="sample_rate_changed")
    ain_buffer_size_changed = Signal(int, name="ain_buffer_size_changed")
    analog_in_bits_changed = Signal(int, name="analog_in_bits_changed")
    analog_in_buffer_size_changed = Signal(int, name="analog_in_buffer_size_changed")
    analog_in_channel_range_changed = Signal(tuple, name="analog_in_channel_range_changed")
    analog_in_offset_changed = Signal(tuple, name="analog_in_offset_changed")

    open_device_finished = Signal(int, name="open_device_finished")
    close_device_finished = Signal(name="close_device_finished")

    device_state_changed = Signal(AD2Constants.DeviceState, name="device_state_changed")

    capture_process_state_changed = Signal(AD2Constants.CapturingState, name="capture_process_state_changed")
    ready_for_recording_changed = Signal(bool, name="ready_for_recording_changed")

    def __init__(self, ad2capt_model: AD2ScopeModel, start_capture_flag: Value):
        super().__init__()

        self.model = ad2capt_model

        self.pref = "AD2CaptDev"

        self.thread_manager = QThreadPool()
        self.kill_thread = False

        self.lock = Lock()
        self.stream_data_queue = Queue()

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
            self.start_capture_flag,
            self.kill_capture_flag
        )
        self.logger.setLevel(logging.INFO)
        self.set_child_log_level(logging.INFO)

        self.connect_signals()
        self._connect_config_signals()

        self.discover_connected_devices()

        self.selected_ain_channel = self.model.analog_in.selected_ain_channel

        # Some Signals and slots to connect
        self.model.supervisor_information.signals.supervised_changed.connect(self._on_supervised_changed)
        self.model.supervisor_information.signals.supervisor_name_changed.connect(self._on_supervisor_name_changed)

    # Supervision slots
    def _on_supervised_changed(self):
        self.logger.info(f"Device is now supervised.")

    def _on_supervisor_name_changed(self, name: str):
        self.logger.info(f"Device is supervised by {name}")

    def connect_signals(self):
        self.dwf_version_changed.connect(self._on_dwf_version_changed)
        self.discovered_devices_changed.connect(self.on_discovered_devices_changed)

        self.selected_device_index_changed.connect(self._on_selected_device_index_changed)

        self.device_connected_changed.connect(
            lambda x: type(self.model.device_information).device_connected.fset(self.model.device_information, x))
        self.device_name_changed.connect(
            lambda x: type(self.model.device_information).device_name.fset(self.model.device_information, x))
        self.device_serial_number_changed.connect(
            lambda x: type(self.model.device_information).device_serial_number.fset(self.model.device_information, x))

        self.ain_channels_changed.connect(
            lambda x: type(self.model.analog_in).ain_channels.fset(self.model.analog_in, x))
        # self.selected_ain_channel_changed.connect(
        #    lambda x: type(self.model.analog_in).selected_ain_channel.fset(self.model.analog_in, x))
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
        self.capture_process_state_changed.connect(self._on_capture_process_state_changed)
        self.ready_for_recording_changed.connect(
            lambda x: type(self.model.capturing_information).ready_for_recording.fset(
                self.model.capturing_information, x))

        self.open_device_finished.connect(self.on_open_device_finished)

    def _connect_config_signals(self):
        self.model.ad2captdev_config.streaming_history.connect(self._on_streaming_history_changed)
        # self.model.ad2captdev_config.selected_device_index.connect(self._on_selected_device_index_changed)

    # ==================================================================================================================
    #   Device control
    # ==================================================================================================================
    @mpPy6.CProcessControl.register_function()
    def set_selected_ain_channel(self, ain_channel_index: int):
        """ Sets the selected analog in channel."""

    @mpPy6.CProcessControl.register_function()
    def set_selected_device(self, device_index: int):
        """
        Sets the selected device index.
        :param device_index: The index of the device.
        """
        self.model.device_information.selected_device_index = device_index

    @mpPy6.CProcessControl.register_function()
    def set_sample_rate(self, sample_rate: float):
        """
        Sets the sample rate.
        :param sample_rate: The sample rate.
        """

    @mpPy6.CProcessControl.register_function(open_device_finished)
    def open_device(self):
        """
        Opens the device with the given id.
        :param device_id:
        :return:
        """
        self.set_sample_rate(self.model.capturing_information.sample_rate)
        self.set_selected_ain_channel(self.model.analog_in.selected_ain_channel)

    def on_open_device_finished(self, device_handle: int):
        self.logger.info(f"Opening device finished with handle {device_handle}")
        self.start_capturing_process()

    @mpPy6.CProcessControl.register_function(close_device_finished)
    def close_device(self):
        self.kill_capture_flag.value = int(True)
        print("Closing device")
        # self.close_device()

    @mpPy6.CProcessControl.register_function(capture_process_state_changed)
    def start_capturing_process(self):
        """
        Starts the capturing process.
        :param sample_rate:
        :param ain_channel:
        :return:
        """
        self.kill_capture_flag.value = int(False)
        self.streaming_dqueue = deque(maxlen=self.model.capturing_information.streaming_deque_length)
        self.thread_manager.start(self.qt_stream_data)

    def stop_capturing_process(self):
        self.kill_capture_flag.value = int(True)

    def _on_streaming_history_changed(self, history: float):
        self.streaming_dqueue = deque(maxlen=self.model.capturing_information.streaming_deque_length)

    # ==================================================================================================================
    # DWF Version
    # ==================================================================================================================
    def _on_dwf_version_changed(self, version):
        self.logger.info(f"DWF Version returned: {version}")
        self.model.dwf_version = version

    # ==================================================================================================================
    #   Discover connected devices
    # ==================================================================================================================
    @mpPy6.CProcessControl.register_function(discovered_devices_changed)
    def discover_connected_devices(self):
        """
            Discover connected devices and update the model.
            :return:
        """

    def on_discovered_devices_changed(self, devices: list):
        self.logger.info(f"Discovered devices: {len(devices)}")
        self.logger.debug(f"Discovered devices: {devices}")
        self.model.device_information.connected_devices = devices

    def _on_selected_device_index_changed(self, index):
        self.model.device_information.selected_device_index = index

    @abstractmethod
    def update_device_information(self):
        raise NotImplementedError

    @abstractmethod
    def _capture(self):
        raise NotImplementedError

    def _on_capture_process_state_changed(self, state):
        self.model.capturing_information.device_capturing_state = state
    
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

    def set_recorded_data_time_axis(self, func=None):

        # Create a new column same as the index
        self.model.capturing_information.recorded_samples_df['time (s)'] = (
            self.model.capturing_information.recorded_samples_df.index.to_series().apply(
                lambda x: x / self.model.capturing_information.sample_rate
            )
        )

        self.model.capturing_information.recorded_samples_df['time (ms)'] = (
            self.model.capturing_information.recorded_samples_df.index.to_series().apply(
                lambda x: (x / self.model.capturing_information.sample_rate) * 1000
            )
        )

    def create_dataframe(self):

        self.model.capturing_information.recorded_samples_df = (
            self.model.capturing_information.capture.to_frame(
                columns=['Amplitude']
            )
        )

        self.set_recorded_data_time_axis()

        if self.model.supervisor_information.supervised:
            try:
                self.model.capturing_information.recorded_samples_df = (
                    self.model.supervisor_information.process_capture(
                        self.model.capturing_information.recorded_samples_df
                    )
                )
            except AttributeError as e:
                self.logger.info(f"Supervisor could not process capture: {e}")

    def stop_capture(self):
        self.start_capture_flag.value = 0

    def start_capture(self, clear=True):
        self.start_capture_flag.value = 1

    def reset_capture(self):
        self.logger.info(f"[{self.pref} Task] Resetting capture...")
        self.stop_capture()
        self.model.capturing_information.capture = (
            self.model.capturing_information.capture.clear()
        )
        if self.model.capturing_information.device_capturing_state == AD2Constants.CapturingState.RUNNING():
            self.start_capture()
        self.model.measurement_time = 0

    # ==================================================================================================================
    def start_device_process(self):
        self.logger.info(f"[{self.pref} Task] Starting capturing process...")

    def qt_stream_data(self):
        self.logger.info("Streaming data thread started")
        while not self.kill_thread:
            if not self.stream_data_queue.empty():
                self.logger.debug(f"Streaming data queue size: {self.stream_data_queue.qsize()}")
                d = self.stream_data_queue.get(block=True, timeout=1)
                self.model.capturing_information.stream.append(d)
                if self.start_capture_flag.value == 1:
                    self.model.capturing_information.capture.append(d)
        self.logger.info("Streaming data thread ended")

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
        for c in self.thread_manager.children():
            c.exit()
        self.safe_exit()
