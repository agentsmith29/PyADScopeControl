from ctypes import c_int, Array

from PySide6.QtCore import QObject, Signal

from ADScopeControl.CaptDeviceConfig import CaptDeviceConfig
from ADScopeControl.model.AD2Constants import AD2Constants


class AD2CaptDeviceInformationSignals(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)


    # Connected Device Information
    num_of_connected_devices_changed = Signal(int)
    connected_devices_changed = Signal(list)
    selected_device_index_changed = Signal(int)

    # Device information
    device_connected_changed = Signal(bool)
    device_name_changed = Signal(str)
    device_serial_number_changed = Signal(str)
    device_index_changed = Signal(int)
    device_state_changed = Signal(AD2Constants.DeviceState)


class AD2CaptDeviceInformationModel:
    def __init__(self, config: CaptDeviceConfig):
        self.signals = AD2CaptDeviceInformationSignals()
        self._config = config
        # Connected Device Information
        self._num_of_connected_devices: int = 0
        self._connected_devices: list = []

        # Device Information
        #self._selected_device_index: int = 0
        self._device_connected: bool = False
        self._device_name: str = "Unknown"
        self._device_serial_number: str = "Unknown"
        self._device_state: AD2Constants.DeviceState = AD2Constants.DeviceState.ACQ_NOT_STARTED()

    # ==================================================================================================================
    # Connected Device Information
    # ==================================================================================================================
    @property
    def num_of_connected_devices(self) -> int:
        return self._num_of_connected_devices

    @num_of_connected_devices.setter
    def num_of_connected_devices(self, value: c_int or int):
        if isinstance(value, c_int):
            self._num_of_connected_devices = int(value.value)
        else:
            self._num_of_connected_devices = int(value)
        self.signals.num_of_connected_devices_changed.emit(self._num_of_connected_devices)

    @property
    def connected_devices(self) -> list:
        return self._connected_devices

    @connected_devices.setter
    def connected_devices(self, value: list):
        self._connected_devices = value
        self.signals.connected_devices_changed.emit(self.connected_devices)

    @property
    def selected_device_index(self) -> int:
        return self._config.selected_device_index.get()

    @selected_device_index.setter
    def selected_device_index(self, value: int):
        self._config.selected_device_index.set(value)
        self.signals.selected_device_index_changed.emit(self.selected_device_index)

    # ==================================================================================================================
    # Device Information
    # ==================================================================================================================
    @property
    def device_connected(self):
        return self._device_connected

    @device_connected.setter
    def device_connected(self, value):
        self._device_connected = value
        self.signals.device_connected_changed.emit(self._device_connected)

    @property
    def device_name(self) -> str:
        return self._device_name

    @device_name.setter
    def device_name(self, value: Array or str):
        if not isinstance(value, str):
            self._device_name = str(value.value.decode('UTF-8'))
        else:
            self._device_name = str(value)
        self.signals.device_name_changed.emit(self.device_name)

    @property
    def device_serial_number(self) -> str:
        return self._device_serial_number

    @device_serial_number.setter
    def device_serial_number(self, value: Array or str):
        if not isinstance(value, str):
            self._device_serial_number = str(value.value.decode('UTF-8'))
        else:
            self._device_serial_number = str(value)
        (self.signals.

         device_serial_number_changed.emit(self.device_serial_number))

    @property
    def device_index(self) -> int:
        return self._device_index

    @device_index.setter
    def device_index(self, value: c_int or int):
        if isinstance(value, c_int):
            self._device_index = int(value.value)
        else:
            self._device_index = int(value)
        self.signals.device_serial_number_changed.emit(self.device_index)

    @property
    def device_state(self) -> AD2Constants.DeviceState:
        return self._device_state

    @device_state.setter
    def device_state(self, value: AD2Constants.DeviceState):
        self._device_state = value
        self.signals.device_state_changed.emit(self.device_state)
