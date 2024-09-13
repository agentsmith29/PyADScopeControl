from ctypes import c_int, Array

from PySide6.QtCore import QObject, Signal

from ADScopeControl.CaptDeviceConfig import CaptDeviceConfig
from ADScopeControl.model.AD2Constants import AD2Constants


class AD2CaptDeviceSupervisorSignals(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    # Connected Device Information
    supervised_changed = Signal(bool)
    supervisor_name_changed = Signal(str)

    supervisor_changed = Signal()
    supervisor_model_changed = Signal()


class AD2CaptDeviceSupervisorModel:
    def __init__(self):
        self.signals = AD2CaptDeviceSupervisorSignals()

        self._supervised: bool = False
        self._supervisor_name: str = "No Supervisor"

        self._supervisor: object = None
        self._supervisor_model: object = None

        self._wl_sweep_start: float = 0.0
        self._wl_sweep_stop: float = 0.0
        self._velocity: float = 0.0
        self._acceleration: float = 0.0
        self._deceleration: float = 0.0

    # ==================================================================================================================
    # Connected Device Information
    # ==================================================================================================================
    @property
    def supervised(self) -> bool:
        return self._supervised

    @supervised.setter
    def supervised(self, value: bool):
        self._supervised = value
        self.signals.supervised_changed.emit(self.supervised)

    @property
    def supervisor_name(self) -> str:
        return self._supervisor_name

    @supervisor_name.setter
    def supervisor_name(self, value: str):
        self._supervisor_name = value
        self.signals.supervisor_name_changed.emit(self.supervisor_name)

    @property
    def supervisor(self) -> object:
        return self._supervisor

    @supervisor.setter
    def supervisor(self, value: object):
        self._supervisor = value
        self.supervisor_name = value.__class__.__name__
        self.supervisor_model = value.model
        self.signals.supervisor_changed.emit()

    @property
    def supervisor_model(self) -> object:
        return self._supervisor_model

    @supervisor_model.setter
    def supervisor_model(self, value: object):
        self._supervisor_model = value
        self.signals.supervisor_model_changed.emit()

    @property
    def sweep_start_wavelength(self) -> float:
        return self._wl_sweep_start

    @sweep_start_wavelength.setter
    def sweep_start_wavelength(self, value: float):
        self._wl_sweep_start = value


    @property
    def sweep_stop_wavelength(self) -> float:
        return self._wl_sweep_stop

    @sweep_stop_wavelength.setter
    def sweep_stop_wavelength(self, value: float):
        self._wl_sweep_stop = value

    @property
    def velocity(self) -> float:
        return self._velocity

    @velocity.setter
    def velocity(self, value: float):
        self._velocity = value

    @property
    def acceleration(self) -> float:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value: float):
        self._acceleration = value

    @property
    def deceleration(self) -> float:
        return self._deceleration

    @deceleration.setter
    def deceleration(self, value: float):
        self._deceleration = value