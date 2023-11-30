import cmp
from PySide6.QtCore import Signal

from CaptDeviceControl.controller.mp_AD2Capture.MPCaptDevice import MPCaptDevice
from model.AD2CaptDeviceModel import AD2CaptDeviceSignals, AD2CaptDeviceModel


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

    def __init__(self,
                 model: AD2CaptDeviceModel,
                 streaming_data_queue,
                 capturing_data_queue,
                 start_capture_flag,
                 parent=None,
                 enable_logging=False):
        super().__init__(parent, enable_logging=enable_logging)
        self.register_child_process(
            MPCaptDevice(self.state_queue, self.cmd_queue,
                         streaming_data_queue,
                         capturing_data_queue,
                         start_capture_flag,
                         enable_logging=enable_logging))

        self.connected_devices_changed.connect(lambda x: type(model).connected_devices.fset(model, x))
        self.ain_channels_changed.connect(lambda x: type(model).ain_channels.fset(model, x))
        self.ain_buffer_size_changed.connect(lambda x: type(model).ain_buffer_size.fset(model, x))
        self.dwf_version_changed.connect(lambda x: type(model).dwf_version.fset(model, x))
        self.device_name_changed.connect(lambda x: type(model).device_name.fset(model, x))
        self.device_serial_number_changed.connect(lambda x: type(model).device_serial_number.fset(model, x))
        self.connected_changed.connect(lambda x: type(model).connected.fset(model, x))


    @cmp.CProcessControl.register_function()
    def connected_devices(self):
        self._internal_logger.info("Discovering connected devices.")

    @cmp.CProcessControl.register_function()
    def ain_channels(self, device_id):
        self._internal_logger.info(f"Reading available analog input channels for device {device_id}.")

    @cmp.CProcessControl.register_function()
    def open_device(self, device_index):
        self._internal_logger.info(f"Opening device {device_index}.")

    @cmp.CProcessControl.register_function()
    def close_device(self):
        self._internal_logger.info(f"Closing device device.")

    @cmp.CProcessControl.register_function()
    def start_capture(self, sample_rate, ain_channel):
        print(f"Starting capture with sample rate {sample_rate} and ain channel {ain_channel}.")
