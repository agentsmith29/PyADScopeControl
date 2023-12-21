from ctypes import c_int, Array

from PySide6.QtCore import QObject, Signal

from CaptDeviceControl.model.AD2Constants import AD2Constants
from CaptDeviceControl.CaptDeviceConfig import CaptDeviceConfig as Config
from model.submodels.AD2CaptDeviceAnalogInModel import AD2CaptDeviceAnalogInModel
from model.submodels.AD2CaptDeviceCapturingModel import AD2CaptDeviceCapturingModel
from model.submodels.AD2CaptDeviceInformationModel import AD2CaptDeviceInformationModel


# from MeasurementData.Properties.AD2CaptDeviceProperties import AD2CaptDeviceProperties


class AD2CaptDeviceSignals(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)


    ad2captdev_config_changed = Signal(Config)

    # WaveForms Runtime (DWF) Information
    dwf_version_changed = Signal(str)

    # Acquisition Settings
    sample_rate_changed = Signal(int)
    streaming_rate_changed = Signal(int)

    duration_streaming_history_changed = Signal(int)

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

    device_state_changed = Signal(AD2Constants.DeviceState)

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
        self.ad2captdev_config.autosave(enable=True, path="./")

        # WaveForms Runtime (DWF) Information
        self._dwf_version: str = "Unknown"
        # Multiprocessing Information
        self._pid: int = 0

        self.device_information = AD2CaptDeviceInformationModel()
        self.analog_in = AD2CaptDeviceAnalogInModel(self.ad2captdev_config)
        self.capturing_information = AD2CaptDeviceCapturingModel(self.ad2captdev_config)
        # Acquisition Settings

        # Analog Out Information
        self.aout_channels: list = []





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
    def device_state(self) -> AD2Constants.DeviceState:
        return self._device_state

    @device_state.setter
    def device_state(self, value: AD2Constants.DeviceState):
       #print(f"Set device_state to {value}")
        self._device_state = value
        self.signals.device_state_changed.emit(self._device_state)


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
    # def ad2_properties(self) -> AD2CaptDeviceProperties:
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
