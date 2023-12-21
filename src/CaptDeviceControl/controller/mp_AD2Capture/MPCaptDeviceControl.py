import logging
import os

import cmp
from PySide6.QtCore import Signal


from CaptDeviceControl.model.AD2CaptDeviceModel import AD2CaptDeviceSignals, AD2CaptDeviceModel
from CaptDeviceControl.model.AD2Constants import AD2Constants

class MPCaptDeviceControl(cmp.CProcessControl):



    connected_devices_changed = Signal(list, name="connected_devices_changed")




    device_capturing_state_changed = Signal(AD2Constants.CapturingState, name="device_capturing_state_changed")


    open_device_finished = Signal(name="open_device_finished")
    close_device_finished = Signal(name="close_device_finished")

    analog_in_bits_changed = Signal(int, name="analog_in_bits_changed")
    analog_in_buffer_size_changed = Signal(int, name="analog_in_buffer_size_changed")
    analog_in_channel_range_changed = Signal(tuple, name="analog_in_channel_range_changed")
    analog_in_offset_changed = Signal(tuple, name="analog_in_offset_changed")

    device_capturing_changed = Signal(bool, name="device_capturing_changed")

    def __init__(self,
                 model: AD2CaptDeviceModel,
                 streaming_data_queue,
                 capturing_data_queue,
                 start_capture_flag,
                 kill_capture_flag,
                 parent=None,
                 internal_log=True,
                 internal_log_level=logging.DEBUG):
        super().__init__(parent,
                         internal_log=internal_log,
                         internal_log_level=internal_log_level)
        self.model = model
        self.register_child_process(
            MPCaptDevice,
                         streaming_data_queue,
                         capturing_data_queue,
                         start_capture_flag,
                         kill_capture_flag
        )

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
        self.device_capturing_state_changed.connect(
            lambda x: type(model).device_capturing_state.fset(model, x))
        self.device_state_changed.connect(
            lambda x: type(model).device_state.fset(model, x))

        # Analog In Information


        self.device_capturing_changed.connect(self.on_capturing_state_changed)

    def on_capturing_state_changed(self, capturing: bool):
        if capturing:
            self.model.device_capturing_state = AD2Constants.CapturingState.RUNNING()
        else:
            self.model.device_capturing_state = AD2Constants.CapturingState.STOPPED()

    @cmp.CProcessControl.register_function(connected_devices_changed)
    def connected_devices(self):
        self.logger.info("Discovering connected devices.")

    # Setter for the selected device index
    @cmp.CProcessControl.register_function()
    def selected_device_index(self, device_index: int):
        self.logger.info(f"Selected device index {device_index}.")

    #@cmp.CProcessControl.register_function(ain_channels_changed)
    #def ain_channels(self, device_id):
    #    self.logger.info(f"Reading available analog input channels for device {device_id}.")

    @cmp.CProcessControl.register_function(open_device_finished)
    def open_device(self, device_index):
        self.logger.info(f"Opening device {device_index}.")

    @cmp.CProcessControl.register_function()
    def close_device(self):
        self.logger.info(f"Closing device device.")

    @cmp.CProcessControl.register_function()
    def start_capture(self, sample_rate, ain_channel):
        print(f"Starting capture with sample rate {sample_rate} and ain channel {ain_channel}.")
