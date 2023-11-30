"""
File for methods that run the multiporcessing capture.
Here we can init the device capturing and stream the data using ques.
(c) Christoph Schmidt, 2023
christoph.schmidt@tugraz.at
"""

import os
import random
import sys
import time
from ctypes import c_int, byref, c_double, cdll, create_string_buffer, c_int32, CDLL

from CaptDeviceControl.controller.mp_AD2Capture.AD2StateMPSetter import AD2StateMPSetter
from CaptDeviceControl.model.AD2Constants import AD2Constants
from CaptDeviceControl.constants.dwfconstants import acqmodeRecord, DwfStateConfig, DwfStatePrefill, DwfStateArmed, enumfilterType, \
    enumfilterUSB, enumfilterDemo


# ======================================================================================================================
# Process logging function
# ======================================================================================================================
def _mp_log_debug(msg, prefix="AD2 Thread"):
    print(f"DBG  | [{prefix}/{os.getpid()}]: {msg}")


def _mp_log_error(msg, prefix="AD2 Thread"):
    print(f"ERR  | [{prefix}/{os.getpid()}]: {msg}")


def _mp_log_info(msg, prefix="AD2 Thread"):
    print(f"INF  | [{prefix}/{os.getpid()}]: {msg}")


def _mp_log_warning(msg, prefix="AD2 Thread"):
    print(f"WARN | [{prefix}/{os.getpid()}]: {msg}")


# ======================================================================================================================
# Process Main function, used for capturing and streaming data
# ======================================================================================================================
def mp_capture(stream_data_queue, capture_data_queue, state_queue,
               start_capture, end_process,
               device_id, channel, sample_rate):
    """
    Captures data from the device and puts it into a queue.
    :param capture_data_queue:
    :param state_queue:
    :param start_capture:
    :param end_process:
    :param device_id:
    :param sample_rate:
    :param stream_data_queue: Queue to put the data into.
    :param channel: Channel to capture data from.
    :return: None
    """

    time_capture_started = 0
    capturing_notified = False

    ad2_state = AD2StateMPSetter(state_queue)
    ad2_state.pid = os.getpid()
    ad2_state.ppid = os.getppid()
    # Print pid and ppid
    _mp_log_info(f"Starting capture thread, pid={ad2_state.pid}, ppid={ad2_state.ppid}")

    ad2_state.selected_ain_channel = channel
    ad2_state.sample_rate = sample_rate
    ad2_state.device_index = device_id
    _mp_log_debug(f"Setting up device {ad2_state.device_index} with "
                  f"channel {ad2_state.selected_ain_channel} and "
                  f"acquisition rate {ad2_state.sample_rate} Hz")

    dwf, hdwf = _mp_open_device(device_id, ad2_state)

    # acquisition_state = c_byte()

    cAvailable = c_int()
    cLost = c_int()
    cCorrupted = c_int()

    # FDwfAnalogInStatus(HDWF hdwf, BOOL fReadData, DwfState* psts)
    _t_setup_aquisition(dwf, hdwf, ad2_state)
    _t_setup_sine_wave(dwf, hdwf, ad2_state)

    _mp_log_info("Configuring acquisition. Starting oscilloscope.")
    # FDwfAnalogInConfigure(HDWF hdwf, int fReconfigure, int fStart)
    # Configures the instrument and start or stop the acquisition. To reset the Auto trigger timeout, set
    # fReconfigure to TRUE.
    # hdwf – Interface handle.
    # fReconfigure – Configure the device.
    # fStart – Start the acquisition.
    dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

    _mp_log_info("Device configured. Starting acquisition.")

    cSamples = 0
    ad2_state.device_ready = True
    capture_samples = 0
    print(end_process.value)
    while end_process.value == int(False):
        # Checks the state of the acquisition. To read the data from the device, set fReadData to TRUE. For
        # single acquisition mode, the data will be read only when the acquisition is finished
        dwf.FDwfAnalogInStatus(hdwf, c_int(1),
                               byref(ad2_state.ain_device_state))  # Variable to receive the acquisition state

        if cSamples == 0 and (
                ad2_state.ain_device_state == DwfStateConfig or
                ad2_state.ain_device_state == DwfStatePrefill or
                ad2_state.ain_device_state == DwfStateArmed):
            _mp_log_info("Device in idle state. Waiting for acquisition to start.")
            continue  # Acquisition not yet started.

        dwf.FDwfAnalogInStatusRecord(hdwf,
                                     byref(cAvailable),
                                     byref(cLost),
                                     byref(cCorrupted))
        cSamples += cLost.value

        if cLost.value:
            ad2_state.samples_lost += cLost.value
        if cCorrupted.value:
            ad2_state.samples_corrupted += cCorrupted.value

        # self.dwf.FDwfAnalogInStatusSamplesValid(self.hdwf, byref(self.cValid))
        if cAvailable.value == 0:
            continue
        else:
            # print(f"Available: {cAvailable.value}")
            # if cSamples + cAvailable.value > self.ad2capt_model.n_samples:
            #    cAvailable = c_int(self.ad2capt_model.n_samples - cSamples)
            rgdSamples = (c_double * cAvailable.value)()

            dwf.FDwfAnalogInStatusData(hdwf, c_int(ad2_state.selected_ain_channel), byref(rgdSamples),
                                       cAvailable)  # get channel data
            # Print how many samples are available
            status = {"available": cAvailable.value, 'captured': 0, 'lost': cLost.value,
                      'corrupted': cCorrupted.value, "time": time.time()}
            #print(status)
            time.sleep(random.random())
            #print(len(rgdSamples))
            stream_data_queue.put(
                ([(float(s)) for s in rgdSamples], status)
            )

            if start_capture.value == 1:
                if not capturing_notified:
                    time_capture_started = time.time()
                    capture_samples = 0
                    _mp_log_info("Starting command recieved. Acquisition started.")
                    ad2_state.acquisition_state = AD2Constants.CapturingState.RUNNING()
                    capturing_notified = True
                capture_samples = capture_samples + len(rgdSamples)
                status = {
                    "available": cAvailable.value,
                    "captured": capture_samples,
                    "lost": cLost.value,
                    "corrupted": cCorrupted.value,
                    "recording_time": time.time() - time_capture_started}
                capture_data_queue.put(([float(s) for s in rgdSamples], status))
                # capture_data_queue.put([float(s) for s in rgdSamples])
            elif start_capture.value == 0:
                if capturing_notified:
                    ad2_state.acquisition_state = AD2Constants.CapturingState.STOPPED()
                    time_capture_stopped = time.time()
                    time_captured = time_capture_stopped - time_capture_started
                    ad2_state.recording_time = time_captured
                    _mp_log_info(f"Acquisition stopped after {time_captured} seconds. Captured {capture_samples} "
                                 f"samples. Resulting in a time of {capture_samples / ad2_state.sample_rate} s.")
                    status = {
                        "available": cAvailable.value,
                        "captured": capture_samples,
                        "lost": cLost.value,
                        "corrupted": cCorrupted.value,
                        "recording_time": time.time() - time_capture_started}
                    capture_data_queue.put(([float(s) for s in rgdSamples], status))

                    capturing_notified = False
            cSamples += cAvailable.value

    _mp_close_device(dwf, hdwf, channel, ad2_state)


def _mp_update_device_information(dwf, hdwf, ad2_state: AD2StateMPSetter):
    in_channel = c_int()
    out_channel = c_int()
    buffer_size = c_int()
    # Get the  Analog In Channels and Buffer Size
    dwf.FDwfAnalogInChannelCount(hdwf, byref(in_channel))
    ad2_state.ain_channels = list(range(0, int(in_channel.value)))
    dwf.FDwfAnalogInBufferSizeInfo(hdwf, 0, byref(buffer_size))

    # Get the Analog Out Channels and Buffer Size
    ad2_state.analog_analog_in_buffer_size = int(buffer_size.value)
    dwf.FDwfAnalogOutCount(hdwf, byref(out_channel))
    ad2_state.aout_channels = list(range(0, int(out_channel.value)))

    # # Select the first Analog In Channel
    # ad2_state.selected_channel = ad2_state.list_of_analog_in_channels[0]


def _mp_get_dwf_information(dwf, ad2_state: AD2StateMPSetter):
    _mp_log_debug(f"Getting DWF version information...")
    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    ad2_state.dwf_version = version.value.decode("utf-8")
    _mp_log_debug(f"DWF Version: {ad2_state.dwf_version}")

# ======================================================================================================================
# Setup the device
# ======================================================================================================================
def _t_setup_sine_wave(dwf, hdwf, ad2_state: AD2StateMPSetter):
    _mp_log_debug("Generating AM sine wave...")
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(0), c_int(1))  # carrier
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), c_int(0), c_int(1))  # sine
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), c_int(0), c_double(0.1))
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), c_int(0), c_double(1))
    # dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), c_int(0), c_double(0.5))
    # dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(2), c_int(1))  # AM
    # dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), c_int(2), c_int(3))  # triangle
    # dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), c_int(2), c_double(0.1))
    # dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), c_int(2), c_double(50))
    dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1))
    _mp_log_debug("Sine wave on output channel 0 configured.")


def _t_setup_aquisition(dwf, hdwf, ad2_state: AD2StateMPSetter):
    dwf.FDwfAnalogInStatus(hdwf, c_int(1),
                           byref(ad2_state.ain_device_state))  # Variable to receive the acquisition state
    _mp_log_info(f"[Task] Setup for acquisition on channel"
                 f" {ad2_state.selected_ain_channel} with rate {ad2_state.sample_rate} Hz.")
    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(ad2_state.selected_ain_channel), c_int(1))
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(ad2_state.selected_ain_channel), c_double(5))
    dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord)
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(ad2_state.sample_rate))
    dwf.FDwfAnalogInRecordLengthSet(hdwf, 0)  # -1 infinite record length

    # Variable to receive the acquisition state
    dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(ad2_state.ain_device_state))
    _mp_log_info(f"[Task] Wait 2 seconds for the offset to stabilize.")
    # wait at least 2 seconds for the offset to stabilize
    time.sleep(2)
    _mp_log_info(f"[Task] Setup for acquisition done.")


def _mp_discover_connected_devices(dwf):
    _mp_log_info(f"Discovering connected devices...")
    num_of_connected_devices = 0

    devicename = create_string_buffer(64)
    serialnum = create_string_buffer(16)

    for iDevice in enumerate_devices(dwf, show_demo_devices=True):
        dwf.FDwfEnumDeviceName(c_int(iDevice), devicename)
        dwf.FDwfEnumSN(c_int(iDevice), serialnum)
        connected_devices.append({
            'type': type,
            'device_id': int(iDevice),
            'device_name': str(devicename.value.decode('UTF-8')),
            'serial_number': str(serialnum.value.decode('UTF-8'))
        })
        #_mp_log_debug(f"Found {type} device: {devicename.value.decode('UTF-8')} ({serialnum.value.decode('UTF-8')})")
    # print(connected_devices)
    # print(f"Discoverd {len(self.model.connected_devices)} devices.")
    return connected_devices

def enumerate_devices(dwf: CDLL, show_demo_devices=False) -> list:
    """
    Enumerates all connected devices. Function is used to discover all connected, compatible devices.
    Builds an internal list of detected devices filtered by the enumfilter parameter. It must be called
    before using other FDwfEnum functions because they obtain information about enumerated devices
    from this list identified by the device index.
    :param show_demo_devices: Specify if demo devices should be shown.
    :return: A list from 0 to n devices.
    """
    if show_demo_devices:
        enum_filter = c_int32(enumfilterType.value | enumfilterUSB.value | enumfilterDemo.value)
    else:
        enum_filter = c_int32(enumfilterType.value | enumfilterUSB.value)

    cDevice = c_int()
    dwf.FDwfEnum(enum_filter, byref(cDevice))
    return list(range(0, cDevice.value))

def _mp_open_device(ad2_state: AD2StateMPSetter):
    """
    Opens the device and returns the handle.
    :return: Device handle.
    """
    _mp_log_debug(f"Importing dwf library for {sys.platform}...")
    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")
    hdwf = c_int()

    _mp_get_dwf_information(dwf, ad2_state)
    # This is needed, otherwise, the device is not found.
    _mp_discover_connected_devices(dwf)

    # Opens the device specified by idxDevice. The device handle is returned in hdwf. If idxDevice is -1, the
    # first available device is opened.
    _mp_log_info(f"[Task] Opening device #{ad2_state.device_index}...")
    dwf.FDwfDeviceOpen(c_int(ad2_state.device_index), byref(hdwf))

    devicename = create_string_buffer(64)
    serialnum = create_string_buffer(16)

    dwf.FDwfEnumDeviceName(c_int(ad2_state.device_index), devicename)
    dwf.FDwfEnumSN(c_int(ad2_state.device_index), serialnum)

    ad2_state.device_name = str(devicename.value.decode("utf-8"))
    ad2_state.device_serial_number = str(serialnum.value.decode("utf-8")).replace("SN:", "")
    # open device

    if hdwf.value == 0:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        _mp_log_error(f"Failed to open device: {szerr.value}")
        ad2_state.connected = False
        raise Exception(f"Failed to open device: {szerr.value}")
    else:
        _mp_log_info(f"Device opened: {ad2_state.device_name} ({ad2_state.device_serial_number})")
        ad2_state.connected = True

    return dwf, hdwf


def _mp_close_device(dwf, hdwf, channel, ad2_state: AD2StateMPSetter):
    dwf.FDwfAnalogOutReset(hdwf, c_int(channel))
    _mp_log_info(f"[Task] Closing device...")
    dwf.FDwfDeviceClose(hdwf)
    ad2_state.connected = False
    _mp_log_info(f"[Task] Device closed.")
