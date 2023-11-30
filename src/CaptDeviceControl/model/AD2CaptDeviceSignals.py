# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
from PySide6.QtCore import QObject, Signal

from CaptDeviceConfig import CaptDeviceConfig as Config
from controller.DeviceInformation.HWDeviceInformation import HWDeviceInformation
from model.AD2Constants import AD2Constants


class AD2CaptDeviceSignals(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    ad2captdev_config_changed = Signal(Config)

    # WaveForms Runtime (DWF) Information
    dwf_version_changed = Signal(str)

    # Connected Device Information
    num_of_discovered_devices_changed = Signal(int)
    discovered_devices_changed = Signal(list)
    selected_devices_changed = Signal(HWDeviceInformation)

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
