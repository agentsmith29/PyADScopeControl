from ctypes import c_int, c_byte

from PySide6.QtCore import QObject, Signal

from ADScopeControl.CaptDeviceConfig import CaptDeviceConfig


class AD2CaptDeviceAnalogInSignals(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    # Analog In Information
    selected_ain_channel_changed = Signal(int)
    ain_channels_changed = Signal(list)
    ain_bits_changed = Signal(int)
    ain_buffer_size_changed = Signal(int)
    ain_channel_range_changed = Signal(tuple)
    ain_offset_changed = Signal(tuple)
    ain_device_state_changed = Signal(int)


class AD2CaptDeviceAnalogInModel:

    def __init__(self, config: CaptDeviceConfig):
        self.signals = AD2CaptDeviceAnalogInSignals()
        self.config = config
        # Analog In Information
        self._ain_channels: list = []
        self._ain_bits: int = -1
        self._ain_buffer_size: tuple = (-1, -1)
        self._ain_channel_range: tuple = (-1, -1, -1)
        self._ain_offset: tuple = (-1, -1, -1)
        self._ain_device_state: int = -1

    # ==================================================================================================================
    # Analog In Information
    # ==================================================================================================================
    @property
    def selected_ain_channel(self) -> int:
        return self.config.ain_channel.get()

    @selected_ain_channel.setter
    def selected_ain_channel(self, value: int or c_int):
        if isinstance(value, c_int):
            value = int(value.value)
        else:
            value = int(value)
        self.config.ain_channel.set(value)
        self.signals.selected_ain_channel_changed.emit(self.selected_ain_channel)


    @property
    def ain_channels(self) -> list:
        return self._ain_channels

    @ain_channels.setter
    def ain_channels(self, value: list):
        self._ain_channels = value
        self.signals.ain_channels_changed.emit(self.ain_channels)

    @property
    def ain_buffer_size(self) -> tuple:
        return self._ain_buffer_size

    @ain_buffer_size.setter
    def ain_buffer_size(self, value: float):
        self._ain_buffer_size = value
        self.signals.ain_buffer_size_changed.emit(self.ain_buffer_size)

    @property
    def ain_bits(self) -> int:
        return self._ain_bits

    @ain_bits.setter
    def ain_bits(self, value: int):
        self._ain_bits = value
        self.signals.ain_bits_changed.emit(self.ain_bits)

    @property
    def ain_device_state(self) -> int:
        return self._ain_device_state

    @ain_device_state.setter
    def ain_device_state(self, value: c_int or int or c_byte):
        if isinstance(value, c_int) or isinstance(value, c_byte):
            self._ain_device_state = int(value.value)
        else:
            self._ain_device_state = int(value)
        self.signals.ain_device_state_changed.emit(self.ain_device_state)