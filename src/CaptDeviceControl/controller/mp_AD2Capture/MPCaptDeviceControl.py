import os

import cmp
from PySide6.QtCore import Signal

from CaptDeviceControl.controller.mp_AD2Capture.MPCaptDevice import MPCaptDevice
from model.AD2CaptDeviceModel import AD2CaptDeviceSignals, AD2CaptDeviceModel
from model.AD2Constants import AD2Constants


class MPCaptDeviceControl(cmp.CProcessControl):
    connected_devices_changed = Signal(list)
    ain_channels_changed = Signal(list)
    ain_buffer_size_changed = Signal(int)
    dwf_version_changed = Signal(str)
    device_name_changed = Signal(str)
    device_serial_number_changed = Signal(str)
    connected_changed = Signal(bool)

    open_device_finished = Signal()
    close_device_finished = Signal()

    analog_in_bits_changed = Signal(int)
    analog_in_buffer_size_changed = Signal(int)
    analog_in_channel_range_changed = Signal(tuple)
    analog_in_offset_changed = Signal(tuple)

    device_capturing_changed = Signal(bool)

    def __init__(self,
                 model: AD2CaptDeviceModel,
                 streaming_data_queue,
                 capturing_data_queue,
                 start_capture_flag,
                 kill_capture_flag,
                 parent=None,
                 enable_internal_logging=False):
        super().__init__(parent, enable_internal_logging=enable_internal_logging)
        self.model = model
        self.register_child_process(
            MPCaptDevice(self.state_queue, self.cmd_queue,
                         streaming_data_queue,
                         capturing_data_queue,
                         start_capture_flag,
                         kill_capture_flag,
                         enable_internal_logging=enable_internal_logging))

        self.logger, self.logger_handler = self.create_new_logger(f"{self.__class__.__name__}({os.getpid()})")

        self.connected_devices_changed.connect(
            lambda x: type(model.device_information).connected_devices.fset(model.device_information, x))
        self.dwf_version_changed.connect(
            lambda x: type(model).dwf_version.fset(model, x))
        self.device_name_changed.connect(
            lambda x: type(model.device_information).device_name.fset(model.device_information, x))
        self.device_serial_number_changed.connect(
            lambda x: type(model.device_information).device_serial_number.fset(model.device_information, x))
        self.connected_changed.connect(
            lambda x: type(model.device_information).device_connected.fset(model.device_information, x))

        # Analog In Information
        self.ain_channels_changed.connect(lambda x: type(model.analog_in).ain_channels.fset(model.analog_in, x))
        self.ain_buffer_size_changed.connect(lambda x: type(model.analog_in).ain_buffer_size.fset(model.analog_in, x))
        self.analog_in_bits_changed.connect(lambda x: type(model.analog_in).ain_bits.fset(model.analog_in, x))
        self.analog_in_buffer_size_changed.connect(lambda x: type(model.analog_in).ain_buffer_size.fset(model.analog_in, x))
        self.analog_in_channel_range_changed.connect(lambda x: type(model.analog_in).ai.fset(model.analog_in, x))
        self.analog_in_offset_changed.connect(lambda x: type(model.analog_in).ain_offset.fset(model.analog_in, x))

        self.device_capturing_changed.connect(self.on_capturing_state_changed)

    def on_capturing_state_changed(self, capturing: bool):
        if capturing:
            self.model.device_capturing_state = AD2Constants.CapturingState.RUNNING()
        else:
            self.model.device_capturing_state = AD2Constants.CapturingState.STOPPED()

    @cmp.CProcessControl.register_function()
    def connected_devices(self):
        self.logger.info("Discovering connected devices.")

    @cmp.CProcessControl.register_function()
    def ain_channels(self, device_id):
        self.logger.info(f"Reading available analog input channels for device {device_id}.")

    @cmp.CProcessControl.register_function()
    def open_device(self, device_index):
        self.logger.info(f"Opening device {device_index}.")

    @cmp.CProcessControl.register_function()
    def close_device(self):
        self.logger.info(f"Closing device device.")

    @cmp.CProcessControl.register_function()
    def start_capture(self, sample_rate, ain_channel):
        print(f"Starting capture with sample rate {sample_rate} and ain channel {ain_channel}.")
