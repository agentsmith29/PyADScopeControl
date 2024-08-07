# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
from PySide6.QtCore import QObject, Signal

from ADScopeControl.CaptDeviceConfig import CaptDeviceConfig as Config
from ADScopeControl.controller.DeviceInformation.HWDeviceInformation import HWDeviceInformation


class AD2CaptDeviceSignals(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    ad2captdev_config_changed = Signal(Config)

    # WaveForms Runtime (DWF) Information
    dwf_version_changed = Signal(str)
    # Multiprocessing Information
    pid_changed = Signal(int)

    # Connected Device Information
    num_of_discovered_devices_changed = Signal(int)
    discovered_devices_changed = Signal(list)
    selected_devices_changed = Signal(HWDeviceInformation)

    # Device information
    connected_changed = Signal(bool)
    device_name_changed = Signal(str)
    serial_number_changed = Signal(str)
    device_index_changed = Signal(int)


    # Analog In Information
    ain_channels_changed = Signal(list)
    ain_buffer_size_changed = Signal(int)
    ain_bits_changed = Signal(int)
    ain_device_state_changed = Signal(int)

    # Analog Out Information
    aout_channels_changed = Signal(list)





