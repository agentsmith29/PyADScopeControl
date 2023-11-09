from ctypes import c_int, Array, c_byte

from PySide6.QtCore import QObject, Signal

from model.AD2Constants import AD2Constants
from CaptDeviceConfig import CaptDeviceConfig as Config
#from MeasurementData.Properties.AD2CaptDeviceProperties import AD2CaptDeviceProperties


class AD2CaptDeviceSignals(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)

    ad2captdev_config_changed = Signal(Config)

    # WaveForms Runtime (DWF) Information
    dwf_version_changed = Signal(str)

    # Connected Device Information
    num_of_connected_devices_changed = Signal(int)
    connected_devices_changed = Signal(list)

    # Device information
    connected_changed = Signal(bool)
    device_name_changed = Signal(str)
    serial_number_changed = Signal(str)
    device_index_changed = Signal(int)

    # Acquisition Settings
    sample_rate_changed = Signal(int)
    streaming_rate_changed = Signal(int)
    selected_ain_channel_changed = Signal(int)
    duration_streaming_history_changed = Signal(int)

    # Analog In Information
    ain_channels_changed = Signal(list)
    ain_buffer_size_changed = Signal(int)
    ain_bits_changed = Signal(int)
    ain_device_state_changed = Signal(int)


    # Analog Out Information
    aout_channels_changed = Signal(list)

    # Acquired Signal Information
    recorded_samples_changed = Signal(list)
    recording_time_changed = Signal(float)
    samples_captured_changed = Signal(int)
    samples_lost_changed = Signal(int)
    samples_corrupted_changed = Signal(int)
    # Actually for the worker, these are the samples that have not been consumed yet by the UI thread.
    unconsumed_stream_samples_changed = Signal(int)
    unconsumed_capture_samples_changed = Signal(int)

    # Recording Flags (starting, stopping and pausing)
    device_capturing_state_changed = Signal(AD2Constants.CapturingState)
    start_recording_changed = Signal(bool)
    stop_recording_changed = Signal(bool)
    reset_recording_changed = Signal(bool)
    capturing_finished_changed = Signal(bool)

    # Multiprocessing Information
    pid_changed = Signal(int)


    # ==================================================================================================================
    # Delete later
    # Signals for device information
    hwdf_changed = Signal(int)


    device_ready_changed = Signal(bool)



    # Signals for reporting if samples were lost or corrupted
    fLost_changed = Signal(int)
    fCorrupted_changed = Signal(int)
    # Acquisition information

    n_samples_changed = Signal(int)

    # Recording settings for starting, stopping and pausing


    # Signal if new samples have been aquired

    all_recorded_samples_changed = Signal(list)
    num_of_current_recorded_samples_changed = Signal(int)
    measurement_time_changed = Signal(float)
    

    ad2_settings = Signal(dict)
    error = Signal(str)
    ad2_is_capturing = Signal(bool)

    ad2_set_acquisition = Signal(bool)
    ad2_captured_value = Signal(list)




class AD2CaptDeviceModel:

    def __init__(self, ad2captdev_config: Config):
        self.signals = AD2CaptDeviceSignals()
        self.ad2captdev_config = ad2captdev_config

        # WaveForms Runtime (DWF) Information
        self._dwf_version: str = "Unknown"

        # Connected Device Information
        self._num_of_connected_devices: int = 0
        self._connected_devices: dict = {}

        # Device Information
        self._connected: bool = False
        self._device_name: str = "Unknown"
        self._device_serial_number: str = "Unknown"
        self._device_index: int = -1

        # Acquisition Settings
        self._sample_rate: int = self.ad2captdev_config.sample_rate.value
        self._streaming_rate: int = self.ad2captdev_config.streaming_rate.value

        self._selected_ain_channel: int = 0
        self._duration_streaming_history: float = 0


        # Analog In Information
        self._ain_channels: list = []
        self._ain_buffer_size: float = -1
        self._ain_device_state: int = -1
        self._ain_bits: int = -1

        # Analog Out Information
        self.aout_channels: list = []

        # Acquired Signal Information
        self._recorded_samples: list = []
        self._recording_time: float = 0
        self._samples_captured: int = 0
        self._samples_lost: int = 0
        self._samples_corrupted: int = 0
        self._capturing_finished: bool = False

        # Actually for the worker, these are the samples that have not been consumed yet by the UI thread.
        self._unconsumed_stream_samples: int = 0
        self._unconsumed_capture_samples: int = 0


        # Recording Flags (starting, stopping and pausing)
        self._device_capturing_state: AD2Constants.CapturingState = AD2Constants.CapturingState.STOPPED()
        self._start_recording = False
        self._stop_recording = True
        self._reset_recording = True

        # Multiprocessing Information
        self._pid: int = 0

        # ==============================================================================================================
        # Delete later
        # Device information
        #
        self._device_ready: bool = False

        self._hwdf = c_int()
        self._auto_connect: bool = False

        self._capturing_finished: bool = False
        # Stores, if samples have been lost or are corrupted
        self._fLost: int = 0
        self._fCorrupted: int = 0
        # List for storing the samples
        # Stores only the current recorded values
        self._measurement_time: float = 0
        # Stores all recorded samples with a timestamp and the measurement time
        self._all_recorded_samples: list = []
        self._num_of_current_recorded_samples: int = 0
        self._n_samples: int = 0



    @property
    def ad2captdev_config(self) -> Config:
        return self._ad2captdev_config

    @ad2captdev_config.setter
    def ad2captdev_config(self, value: Config):
        self._ad2captdev_config = value
        self.signals.ad2captdev_config_changed.emit(self.ad2captdev_config)

    # ==================================================================================================================
    # WaveForms Runtime (DWF) Information
    # ==================================================================================================================
    @property
    def dwf_version(self) -> str:
        return self._dwf_version

    @dwf_version.setter
    def dwf_version(self, value: Array | str):
        if not isinstance(value, str):
            self._dwf_version = str(value.value.decode('UTF-8'))
        else:
            self._dwf_version = value
        self.signals.dwf_version_changed.emit(self.dwf_version)

    # ==================================================================================================================
    # Connected Device Information
    # ==================================================================================================================
    @property
    def num_of_connected_devices(self) -> int:
        return self._num_of_connected_devices

    @num_of_connected_devices.setter
    def num_of_connected_devices(self, value: c_int | int):
        if isinstance(value, c_int):
            self._num_of_connected_devices = int(value.value)
        else:
            self._num_of_connected_devices = int(value)
        self.signals.num_of_connected_devices_changed.emit(self._num_of_connected_devices)

    @property
    def connected_devices(self) -> dict:
        return self._connected_devices

    @connected_devices.setter
    def connected_devices(self, value: dict):
        self._connected_devices = value
        self.signals.connected_devices_changed.emit(self.connected_devices)


    # ==================================================================================================================
    # Device Information
    # ==================================================================================================================
    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value
        self.signals.connected_changed.emit(self._connected)

    @property
    def device_name(self) -> str:
        return self._device_name

    @device_name.setter
    def device_name(self, value: Array | str):
        if not isinstance(value, str):
            self._device_name = str(value.value.decode('UTF-8'))
        else:
            self._device_name = str(value)
        self.signals.device_name_changed.emit(self.device_name)

    @property
    def device_serial_number(self) -> str:
        return self._device_serial_number

    @device_serial_number.setter
    def device_serial_number(self, value: Array | str):
        if not isinstance(value, str):
            self._device_serial_number = str(value.value.decode('UTF-8'))
        else:
            self._device_serial_number = str(value)
        self.signals.serial_number_changed.emit(self.device_serial_number)

    @property
    def device_index(self) -> int:
        return self._device_index

    @device_index.setter
    def device_index(self, value: c_int | int):
        if isinstance(value, c_int):
            self._device_index = int(value.value)
        else:
            self._device_index = int(value)
        self.signals.serial_number_changed.emit(self.device_index)


    # ==================================================================================================================
    # Acquisition Settings
    # ==================================================================================================================
    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = value
        self.ad2captdev_config.sample_rate.set(self._sample_rate)
        self.signals.sample_rate_changed.emit(self._sample_rate)

    @property
    def streaming_rate(self):
        return self._sample_rate

    @streaming_rate.setter
    def streaming_rate(self, value):
        self._streaming_rate = value
        self.ad2captdev_config.streaming_rate.set(self._streaming_rate)
        self.signals.streaming_rate_changed.emit(self._streaming_rate)

    @property
    def selected_ain_channel(self) -> int:
        return self._selected_ain_channel

    @selected_ain_channel.setter
    def selected_ain_channel(self, value: int | c_int):
        if isinstance(value, c_int):
            self._selected_ain_channel = int(value.value)
        else:
            self._selected_ain_channel = int(value)
        self.ad2captdev_config.ain_channel.set(self._selected_ain_channel)
        self.signals.selected_ain_channel_changed.emit(self.selected_ain_channel)

    @property
    def duration_streaming_history(self) -> float:
        return self._duration_streaming_history

    @duration_streaming_history.setter
    def duration_streaming_history(self, value: float):
        self._duration_streaming_history = value
        self.signals.duration_streaming_history_changed.emit(self.duration_streaming_history)

    # ==================================================================================================================
    # Analog In Information
    # ==================================================================================================================
    @property
    def ain_channels(self) -> list:
        return self._ain_channels

    @ain_channels.setter
    def ain_channels(self, value: list):
        self._ain_channels = value
        self.signals.ain_channels_changed.emit(self.ain_channels)

    @property
    def ain_buffer_size(self) -> float:
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
    def ain_device_state(self, value: c_int | int | c_byte):
        if isinstance(value, c_int) or isinstance(value, c_byte):
            self._ain_device_state = int(value.value)
        else:
            self._ain_device_state = int(value)
        self.signals.ain_device_state_changed.emit(self.ain_device_state)

    # ==================================================================================================================
    # Analog Out Information
    # ==================================================================================================================
    @property
    def aout_channels(self) -> list:
        return self._aout_channels

    @aout_channels.setter
    def aout_channels(self, value: list):
        self._aout_channels = value
        self.signals.aout_channels_changed.emit(self.aout_channels)


    # ==================================================================================================================
    # Acquired Signal Information
    # ==================================================================================================================
    @property
    def recorded_samples(self) -> list:
        return self._recorded_samples

    @recorded_samples.setter
    def recorded_samples(self, value: list):
        self._recorded_samples = value
        self.samples_captured = len(self._recorded_samples)
        #self.signals.num_of_current_recorded_samples_changed.emit(self.num_of_current_recorded_samples)
        self.signals.recorded_samples_changed.emit(self.recorded_samples)

    @property
    def recording_time(self) -> float:
        return self._recording_time

    @recording_time.setter
    def recording_time(self, value: float):
        self._recording_time = value
        self.signals.recording_time_changed.emit(self.recording_time)

    @property
    def samples_captured(self) -> int:
        return self._samples_captured

    @samples_captured.setter
    def samples_captured(self, value: int):
        self._samples_captured = value
        self.signals.samples_captured_changed.emit(self.samples_captured)

    @property
    def samples_lost(self) -> int:
        return self._samples_lost

    @samples_lost.setter
    def samples_lost(self, value: int):
        self._samples_lost = value
        self.signals.samples_lost_changed.emit(self.samples_lost)

    @property
    def samples_corrupted(self) -> int:
        return self._samples_corrupted

    @samples_corrupted.setter
    def samples_corrupted(self, value: int):
        self._samples_corrupted = value
        self.signals.samples_corrupted_changed.emit(self.samples_corrupted)


    @property
    def capturing_finished(self) -> bool:
        return self._capturing_finished
    
    @capturing_finished.setter
    def capturing_finished(self, value: bool):
        self._capturing_finished = value
        print(f"Set _capturing_finished to { self._capturing_finished}")
        self.signals.capturing_finished_changed.emit(self._capturing_finished)
        

    # ==================================================================================================================
    # Recording Flags (starting, stopping and pausing)
    # ==================================================================================================================
    @property
    def device_capturing_state(self) -> AD2Constants.CapturingState:
        return self._device_capturing_state

    @device_capturing_state.setter
    def device_capturing_state(self, value: int):
        self._device_capturing_state = value
        self.signals.device_capturing_state_changed.emit(self.device_capturing_state)

    @property
    def start_recording(self) -> bool:
        return self._start_recording

    @start_recording.setter
    def start_recording(self, value: bool):
        self._start_recording = value
        self.signals.start_recording_changed.emit(self._start_recording)

    @property
    def stop_recording(self) -> bool:
        return self._stop_recording

    @stop_recording.setter
    def stop_recording(self, value: bool):
        self._stop_recording = value
        self.signals.stop_recording_changed.emit(self.stop_recording)

    @property
    def reset_recording(self):
        return self._reset_recording

    @reset_recording.setter
    def reset_recording(self, value):
        self._reset_recording = value
        self.signals.reset_recording_changed.emit(self._reset_recording)


    # ==================================================================================================================
    # Multiprocessing Flags
    # ==================================================================================================================
    @property
    def pid(self) -> int:
        return self._pid

    @pid.setter
    def pid(self, value: int):
        self._pid = value
        self.signals.pid_changed.emit(self.pid)

    @property
    def unconsumed_stream_samples(self) -> int:
        return self._unconsumed_stream_samples

    @unconsumed_stream_samples.setter
    def unconsumed_stream_samples(self, value: int):
        self._unconsumed_stream_samples = value
        self.signals.unconsumed_stream_samples_changed.emit(self.unconsumed_stream_samples)

    @property
    def unconsumed_capture_samples(self) -> int:
        return self._unconsumed_capture_samples

    @unconsumed_capture_samples.setter
    def unconsumed_capture_samples(self, value: int):
        self._unconsumed_capture_samples = value
        self.signals.unconsumed_capture_samples_changed.emit(self.unconsumed_capture_samples)



    # ==================================================================================================================
    # ==================================================================================================================
    # DELETE LATER
    # ==================================================================================================================
    # ==================================================================================================================
    @property
    def auto_connect(self) -> bool:
        return self._auto_connect

    @auto_connect.setter
    def auto_connect(self, value: bool):
        self._auto_connect = value

    @property
    #def ad2_properties(self) -> AD2CaptDeviceProperties:
    #    return AD2CaptDeviceProperties(self._fLost, self._fCorrupted,
    #                                   self._sample_rate, self._n_samples,
    #                                   self._measurement_time)

    @property
    def capturing_finished(self) -> bool:
        return self._capturing_finished

    @capturing_finished.setter
    def capturing_finished(self, value: bool):
        self._capturing_finished = value
        self.signals.capturing_finished_changed.emit(self.capturing_finished)

    @property
    def measurement_time(self) -> float:
        return self._measurement_time

    @measurement_time.setter
    def measurement_time(self, value: float):
        self._measurement_time = value
        self.signals.measurement_time_changed.emit(self.measurement_time)

    @property
    def hdwf(self) -> c_int:
        return self._hwdf

    @hdwf.setter
    def hdwf(self, value: c_int):
        self._hwdf = value
        self.signals.hwdf_changed.emit(int(self._hwdf.value))

    @property
    def num_of_current_recorded_samples(self) -> int:
        """Only setter property!"""
        return self._num_of_current_recorded_samples

    @property
    def device_ready(self) -> bool:
        return self._device_ready

    @device_ready.setter
    def device_ready(self, value: bool):
        self._device_ready = value
        self.signals.device_ready_changed.emit(self.device_ready)

    @property
    def all_recorded_samples(self) -> list:
        return self._all_recorded_samples

    @all_recorded_samples.setter
    def all_recorded_samples(self, value: list):
        self._all_recorded_samples = value
        self.signals.all_recorded_samples_changed.emit(self.all_recorded_samples)


    @property
    def n_samples(self):
        return self._n_samples

    @n_samples.setter
    def n_samples(self, value):
        self._n_samples = value
        self.signals.n_samples_changed.emit(self._n_samples)

    @property
    def fCorrupted(self):
        return self._fCorrupted

    @fCorrupted.setter
    def fCorrupted(self, value):
        self._fCorrupted = value
        self.signals.fCorrupted_changed.emit(self._fCorrupted)

    @property
    def fLost(self):
        return self._fLost

    @fLost.setter
    def fLost(self, value):
        self._fLost = value
        self.signals.fLost_changed.emit(self._fLost)


