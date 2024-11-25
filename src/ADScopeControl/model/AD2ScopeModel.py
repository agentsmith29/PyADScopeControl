from ctypes import Array

from PySide6.QtCore import QObject, Signal

from ADScopeControl.CaptDeviceConfig import CaptDeviceConfig as Config
from ADScopeControl.model.AD2Constants import AD2Constants
from ADScopeControl.model.submodels.AD2CaptDeviceAnalogInModel import AD2CaptDeviceAnalogInModel
from ADScopeControl.model.submodels.AD2CaptDeviceCapturingModel import AD2CaptDeviceCapturingModel
from ADScopeControl.model.submodels.AD2CaptDeviceInformationModel import AD2CaptDeviceInformationModel
from ADScopeControl.model.submodels.AD2CaptDeviceSupervisorModel import AD2CaptDeviceSupervisorModel


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
    recording_time_changed = Signal(float)
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

    measurement_time_changed = Signal(float)

    ad2_settings = Signal(dict)
    error = Signal(str)
    ad2_is_capturing = Signal(bool)

    ad2_set_acquisition = Signal(bool)
    ad2_captured_value = Signal(list)


class AD2ScopeModel:

    def __init__(self, ad2captdev_config: Config):
        self.signals = AD2CaptDeviceSignals()
        self.ad2captdev_config = ad2captdev_config
        self.ad2captdev_config.autosave(enable=True, path="./")

        # WaveForms Runtime (DWF) Information
        self._dwf_version: str = "Unknown"
        # Multiprocessing Information
        self._pid: int = 0

        self.device_information = AD2CaptDeviceInformationModel(self.ad2captdev_config)
        self.analog_in = AD2CaptDeviceAnalogInModel(self.ad2captdev_config)
        self.capturing_information = AD2CaptDeviceCapturingModel(self.ad2captdev_config)
        self.supervisor_information = AD2CaptDeviceSupervisorModel()
        # Acquisition Settings

        # Analog Out Information
        self.aout_channels: list = []

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
