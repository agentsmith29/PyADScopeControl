from ctypes import c_int, c_byte

from CaptDeviceControl.model.AD2Constants import AD2Constants

class AD2State:
    def __init__(self):
        # Multiprocessing Information
        self._pid = None
        self._ppid = None

        # WaveForms Runtime (DWF) Information
        self._dwf_version: str = "Unknown"

        # Device information
        self._connected: bool = False
        self._device_name: str = "Unknown"
        self._serial_number: str = "Unknown"
        self._device_index: int = -1

        # Acquisition Settings
        self._sample_rate: int = -1
        self._selected_ain_channel: int = -1

        # Analog In Information
        self._ain_channels: list = []
        self._ain_buffer_size: int = -1
        self._ain_bits: int = -1
        self._ain_device_state: c_byte = c_byte()

        # Analog Out Information
        self._aout_channels: list = []

        # Acquired Signal Information
        self._acquisition_state: int = AD2Constants.CapturingState.STOPPED()

        self._time_capture_started: float = -1  # The time the capturing has started
        self._time_capture_ended: float = -1  # The time the capturing has ended
        self._recording_time: float = -1

        self._samples_captured: int = 0
        self._samples_lost: int = -1
        self._samples_corrupted: int = -1

        # Device Status
        self._device_ready: bool = False
        self._device_capturing = False


    def reinit(self, fields: dict):
        for k, v in fields.items():
            setattr(self, k, v)

    # =========== Multiprocessing Information
    @property
    def pid(self):
        return self._pid

    @property
    def ppid(self):
        return self._ppid

    # =========== WaveForms Runtime (DWF) Information
    @property
    def dwf_version(self):
        return self._dwf_version

    # =========== Device Information
    @property
    def connected(self):
        return self._connected

    @property
    def device_name(self):
        return self._device_name

    @property
    def device_serial_number(self):
        return self._serial_number

    @property
    def device_index(self):
        return self._device_index

    # ========== Acquisition Settings
    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def selected_ain_channel(self):
        return self._selected_ain_channel

    # =========== Analog In Information
    @property
    def ain_channels(self):
        return self._ain_channels

    @property
    def ain_buffer_size(self):
        return self._ain_buffer_size

    @property
    def ain_bits(self):
        return self._ain_bits

    @property
    def ain_device_state(self):
        return self._ain_device_state

    # =========== Analog Out Information
    @property
    def aout_channels(self):
        return self._aout_channels

    # =========== Acquired Signal Information
    @property
    def acquisition_state(self):
        return self._acquisition_state

    @property
    def time_capture_started(self) -> float:
        """The time the capturing has started"""
        return self._time_capture_started

    @property
    def time_capture_ended(self) -> float:
        """The time the capturing has ended"""
        return self._time_capture_ended

    @property
    def recording_time(self):
        return self._recording_time

    @property
    def samples_captured(self):
        return self._samples_captured

    @property
    def samples_lost(self):
        return self._samples_lost

    @property
    def samples_corrupted(self):
        return self._samples_corrupted

    # =========== Device Status
    @property
    def device_ready(self):
        return self._device_ready

    @property
    def device_capturing(self):
        return self._device_capturing


class AD2StateMPSetter(AD2State):

    def __init__(self, state_queue):
        super().__init__()
        self._state_queue = state_queue

    # =========== Multiprocessing Information
    @AD2State.pid.setter
    def pid(self, value):
        self._pid = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.ppid.setter
    def ppid(self, value):
        self._ppid = value
        self._state_queue.put(self.to_simple_class())

    # =========== WaveForms Runtime (DWF) Information
    @AD2State.dwf_version.setter
    def dwf_version(self, value):

        self._dwf_version = value
        self._state_queue.put(self.to_simple_class())

    # =========== Device Information
    @AD2State.connected.setter
    def connected(self, value):
        self._connected = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.device_name.setter
    def device_name(self, value):
        self._device_name = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.device_serial_number.setter
    def device_serial_number(self, value):
        self._serial_number = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.device_index.setter
    def device_index(self, value):
        self._device_index = value
        self._state_queue.put(self.to_simple_class())

    # ========== Acquisition Settings
    @AD2State.sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.selected_ain_channel.setter
    def selected_ain_channel(self, value):
        self._selected_ain_channel = value
        self._state_queue.put(self.to_simple_class())

    # =========== Analog In Information
    @AD2State.ain_channels.setter
    def ain_channels(self, value):
        self._ain_channels = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.ain_buffer_size.setter
    def ain_buffer_size(self, value):
        self._ain_buffer_size = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.ain_bits.setter
    def ain_bits(self, value):
        self._ain_bits = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.ain_device_state.setter
    def ain_device_state(self, value):
        self._ain_device_state = value
        self._state_queue.put(self.to_simple_class())

    # =========== Analog Out Information
    @AD2State.aout_channels.setter
    def aout_channels(self, value):
        self._aout_channels = value
        self._state_queue.put(self.to_simple_class())

    # =========== Acquired Signal Information
    @AD2State.acquisition_state.setter
    def acquisition_state(self, value):
        self._acquisition_state = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.time_capture_ended.setter
    def time_capture_started(self, value: float):
        """The time the capturing has started"""
        self._time_capture_started = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.time_capture_ended.setter
    def time_capture_ended(self, value: float):
        self._time_capture_ended = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.recording_time.setter
    def recording_time(self, value):
        self._recording_time = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.samples_captured.setter
    def samples_captured(self, value):
        self._samples_captured = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.samples_lost.setter
    def samples_lost(self, value):
        self._samples_lost = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.samples_corrupted.setter
    def samples_corrupted(self, value):
        self._samples_corrupted = value
        self._state_queue.put(self.to_simple_class())

    # =========== Device Status
    @AD2State.device_ready.setter
    def device_ready(self, value):
        self._device_ready = value
        self._state_queue.put(self.to_simple_class())

    @AD2State.device_capturing.setter
    def device_capturing(self, value):
        self._device_capturing = value
        self._state_queue.put(self.to_simple_class())

    def to_simple_class(self) -> AD2State:
        exclude = ["_state_queue"]
        ad2state = AD2State()
        to_dict = {}
        for item, value in self.__dict__.items():
            if item in exclude:
                continue
            else:
                to_dict[item] = value
        ad2state.reinit(to_dict)
        return ad2state
