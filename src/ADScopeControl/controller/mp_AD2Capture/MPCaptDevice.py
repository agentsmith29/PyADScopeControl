import sys
import sys
import time
from ctypes import c_int, c_int32, byref, create_string_buffer, cdll, c_double, c_byte
from multiprocessing import Queue, Value

import mpPy6
import numpy as np
from mpPy6.CProperty import CProperty

from ADScopeControl.model.AD2Constants import AD2Constants
from ADScopeControl.constants.dwfconstants import enumfilterType, enumfilterDemo, enumfilterUSB, acqmodeRecord, \
    DwfStateConfig, \
    DwfStatePrefill, DwfStateArmed


class MPCaptDevice(mpPy6.CProcess, ):

    #@staticmethod
    def timeit(func):
        def wrapper(self, *args, **kwargs):
            time_start = time.time()
            res = func(self, *args, **kwargs)
            time_stop = time.time()
            print(f"Function {func.__name__} took {time_stop - time_start} seconds.")
            return res  # time_stop - time_start

        return wrapper

    def __init__(self, state_queue: Queue, cmd_queue: Queue,
                 streaming_data_queue: Queue,
                 start_capture_flag: Value,
                 kill_capture_flag: Value,
                 kill_flag: Value,
                 internal_log, internal_log_level, log_file):
        super().__init__(state_queue, cmd_queue,
                         kill_flag=kill_flag,
                         internal_log=internal_log,
                         internal_log_level=internal_log_level, log_file=log_file)

        # Objects for data exchange
        self.start_capture_flag: Value = start_capture_flag
        self.kill_capture_flag: Value = kill_capture_flag
        self.stream_data_queue = streaming_data_queue

        # WaveForms api objects and handles
        self.dwf = None
        self.hdwf = None

        self._dwf_version = None

        self._connected_devices = []
        self._ain_channels = []

        # Capture data counters
        self._selected_device_index: int = 0
        self._selected_ain_channel: int = 0
        self._sample_rate = 0
        self._connected = False
        self._device_serial_number: str = ""
        self._device_name: str = ""

        self._device_capturing = False
        self._ready_for_recording = False

        # ==============================================================================================================
        self._c_samples = None
        self._c_corrupted = None
        self._c_lost = None
        self._c_available = None
        # ==============================================================================================================
        self._samples_lost = 0
        self._samples_corrupted = 0



    # ==================================================================================================================
    # Getter and Setter
    # ==================================================================================================================
    @CProperty
    def dwf_version(self):
        return self._dwf_version

    @dwf_version.setter(emit_to='dwf_version_changed')
    def dwf_version(self, value):
        self._dwf_version = value

    @CProperty
    def connected_devices(self) -> list:
        """ Returns the list of connected devices."""
        return self._connected_devices

    @connected_devices.setter(emit_to='connected_devices_changed')
    def connected_devices(self, value: list):
        self._connected_devices = value

    @CProperty
    def device_name(self):
        return self._device_name

    @device_name.setter(emit_to='device_name_changed')
    def device_name(self, value):
        self._device_name = value

    @CProperty
    def device_serial_number(self):
        return self._device_serial_number

    @device_serial_number.setter(emit_to='device_serial_number_changed')
    def device_serial_number(self, value):
        self._device_serial_number = value

    @CProperty
    def connected(self):
        return self._connected

    @connected.setter(emit_to='device_connected_changed')
    def connected(self, value):
        self._connected = value

    @CProperty
    def ain_channels(self) -> list:
        return self._ain_channels

    @ain_channels.setter(emit_to='ain_channels_changed')
    def ain_channels(self, value):
        self._ain_channels = value

    @CProperty
    def device_capturing(self):
        return self._device_capturing

    @device_capturing.setter(emit_to='device_capturing_changed')
    def device_capturing(self, capturing: bool):
        self._device_capturing = capturing

    @CProperty
    def selected_ain_channel(self) -> int:
        return self._selected_ain_channel

    @selected_ain_channel.setter(emit_to='selected_ain_channel_changed')
    def selected_ain_channel(self, value: int):
        self.logger.debug(f"Setting selected ain channel to {value}.")
        self._selected_ain_channel = value

    @CProperty
    def sample_rate(self) -> float:
        return self._sample_rate

    @sample_rate.setter(emit_to='sample_rate_changed')
    def sample_rate(self, value):
        self._sample_rate = value

    @CProperty
    def selected_device_index(self):
        """ Returns the selected device index."""
        return self._selected_device_index

    @selected_device_index.setter(emit_to='selected_device_index_changed')
    def selected_device_index(self, device_index: int):
        """ Sets the selected device index."""
        self._selected_device_index = device_index
        # If the selected device index change, we need to update the device information
        self.device_name = self.get_device_name(self._selected_device_index)
        self.device_serial_number = self.get_device_serial_number(self._selected_device_index)

        self.ain_channels = self.get_ain_channels()
        self.ain_buffer_size = self.get_ain_buffer_size(self._selected_device_index)

    @CProperty
    def ready_for_recording(self):
        return self._ready_for_recording

    @ready_for_recording.setter(emit_to='ready_for_recording_changed')
    def ready_for_recording(self, value: bool):
        self._ready_for_recording = value

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def postrun_init(self):
        if sys.platform.startswith("win"):
            self.dwf = cdll.dwf
        elif sys.platform.startswith("darwin"):
            self.dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            self.dwf = cdll.LoadLibrary("libdwf.so")
        # self._connected = self.connected()

        self.dwf_version = self.get_dwf_version()

    # ==================================================================================================================
    # DWF FUnctions
    # ==================================================================================================================
    def get_dwf_version(self) -> str:
        self.logger.debug(f"Getting DWF version information...")
        version = create_string_buffer(16)
        self.dwf.FDwfGetVersion(version)
        return version.value.decode("utf-8")

    # ==================================================================================================================
    # Device Enumeration without connecting to the device
    # ==================================================================================================================
    @mpPy6.CProcess.register_signal()
    def discover_connected_devices(self,
                                   filter_type: int = enumfilterType.value | enumfilterDemo.value | enumfilterUSB.value):

        self.logger.info(f"Discovering connected devices...")
        # enumerate connected devices
        connected_devices = []
        # for filter_type in [(c_int32(enumfilterType.value | enumfilterUSB.value), 'USB'),
        #                     (c_int32(enumfilterType.value | enumfilterNetwork.value), 'Network'),
        #                     (c_int32(enumfilterType.value | enumfilterAXI.value), 'AXI'),
        #                     (c_int32(enumfilterType.value | enumfilterRemote.value), 'Remote'),
        #                     (c_int32(enumfilterType.value | enumfilterAudio.value), 'Audio'),
        #                     (c_int32(enumfilterType.value | enumfilterDemo.value), 'Demo')]:
        cDevice = c_int()
        filter, type = (c_int32(filter_type), 'USB')
        # filter, type = (c_int32(enumfilterType.value | enumfilterDemo.value), 'DEMO')
        self.logger.debug(f"Filter has been used: {hex(int(filter_type))}")
        self.dwf.FDwfEnum(filter, byref(cDevice))

        for iDevice in range(0, cDevice.value):
            if self.get_device_serial_number(iDevice) == "DEMO":
                _type = "DEMO"
            else:
                _type = type
            connected_devices.append({
                'type': _type,
                'device_id': int(iDevice),
                'device_name': self.get_device_name(iDevice),
                'serial_number': self.get_device_serial_number(iDevice)
            })
            # _mp_log_debug(f"Found {type} device: {devicename.value.decode('UTF-8')} ({serialnum.value.decode('UTF-8')})")
        self.logger.debug(f"Found {len(connected_devices)} devices.")
        return connected_devices

    # ==================================================================================================================
    # Settings from process Control
    # ==================================================================================================================

    @mpPy6.CProcess.register_signal()
    def set_selected_ain_channel(self, ain_channel):
        self.selected_ain_channel = ain_channel
        #self.ain_buffer_size = self.get_ain_buffer_size(self._selected_device_index)

    @mpPy6.CProcess.register_signal()
    def set_selected_device(self, ain_channel):
        self.selected_device_index = ain_channel
        # self.ain_buffer_size = self.get_ain_buffer_size(self._selected_device_index)

    @mpPy6.CProcess.register_signal()
    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate

    # ==================================================================================================================
    # Functions for opening and closing the device
    # ==================================================================================================================
    @mpPy6.CProcess.register_signal()
    def open_device(self) -> int:
        """
        Opens the device and returns the handle.
        :return: Device handle.
        """
        if self.hdwf is not None or not isinstance(self.hdwf, c_int):
            self.hdwf = c_int()

        self.logger.debug(f"Opening device {self._selected_device_index}...")
        self._dwf_version = self.get_dwf_version()

        # Opens the device specified by idxDevice. The device handle is returned in hdwf. If idxDevice is -1, the
        # first available device is opened.
        self.dwf.FDwfDeviceOpen(c_int(self._selected_device_index), byref(self.hdwf))

        self._device_name = self.get_device_name(self._selected_device_index)
        self._device_serial_number = self.get_device_serial_number(self._selected_device_index)

        if self.hdwf.value == 0:
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            err = szerr.value.decode("utf-8")
            self.logger.error(f"Failed to open device: {err}")
            # ad2_state.connected = False
            raise Exception(f"Failed to open device: {err}")
        else:
            self.logger.info(f"Device opened: {self._device_name} "
                             f"({self._device_serial_number})")
        self.connected = self.device_connected()
        self.device_state(AD2Constants.DeviceState.ACQ_NOT_STARTED())
        return int(self.hdwf.value)

    @mpPy6.CProcess.register_signal()
    def close_device(self):
        # self.dwf.FDwfAnalogOutReset(self.hdwf, c_int(channel))
        self.logger.debug(f"[Task] Closing device...")
        self.dwf.FDwfDeviceClose(self.hdwf)
        self.hdwf.value = 0
        self.connected = False
        self.logger.info(f"[Task] Device closed.")

    # ==================================================================================================================
    # Device Information
    # ==================================================================================================================
    def get_ain_channels(self) -> list:
        #self.logger.debug(f"Reading available analog input channels for device {self.selected_device_index}.")
        #cInfo = c_int()
        #print(f">>> {cInfo}")
        #self.dwf.FDwfEnumConfigInfo(c_int(self.selected_device_index), c_int(1), byref(cInfo))
        #print(f">>><<<< {cInfo}")
        #self.ain_channels = cInfo.value
        #if self.ain_channels == 0:
        # Sometimes, the device reports a wrong number of ain channels
        # so we can try to connect to the device first and retrieve the information
        self.open_device()
        self.ain_channels = self.analog_in_channels_count()
        self.close_device()
        self.logger.info(f"Device {self.device_name} (#{self.selected_device_index}, SNR: {self.device_serial_number}) "
                         f"AIn: {self.ain_channels}")
        return list(range(0, self.ain_channels))

    def get_ain_buffer_size(self, device_id) -> int:
        cInfo = c_int()
        self.dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(7), byref(cInfo))
        return cInfo.value

    def get_device_name(self, device_index: int) -> str:
        try:
            devicename = create_string_buffer(64)
            self.dwf.FDwfEnumDeviceName(c_int(device_index), devicename)
            return str(devicename.value.decode("utf-8"))
        except Exception as e:
            self.logger.error(f"Error while reading device name: {e}")
            raise Exception(f"Error while reading device name: {e}")

    def get_device_serial_number(self, device_index: int) -> str:
        try:
            serialnum = create_string_buffer(16)
            self.dwf.FDwfEnumSN(c_int(device_index), serialnum)
            return str(serialnum.value.decode("utf-8")).replace("SN:", "")
        except Exception as e:
            self.logger.error(f"Error while reading device serial number: {e}")
            raise Exception(f"Error while reading device serial number: {e}")

    # ==================================================================================================================
    # Device connection status
    # ==================================================================================================================
    def device_connected(self) -> bool:
        if self.hdwf is None or self.hdwf.value == 0:
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            self.logger.error(str(szerr.value))
            return False
        else:
            self.logger.debug(f"Device connected: {self._device_name} ({self._device_serial_number})")
            return True

    # ==================================================================================================================
    # Analog Input Channel Information
    # ==================================================================================================================
    def analog_in_channels_count(self) -> int:
        """
        Reads the number of AnalogIn channels of the device. The oscilloscope channel settings are
        identical across all channels.
        Calls WaveForms API Function 'FDwfAnalogInChannelCount(HDWF hdwf, int *pcChannel)'
        :return: The number of analog in channels.
        """
        if self.device_connected():
            self.logger.debug(f"Reading AnalogIn Channel Count from device {self._device_name}")
            try:
                int0 = c_int()
                self.dwf.FDwfAnalogInChannelCount(self.hdwf, byref(int0))
                _analog_in_channels = int(int0.value)
                return _analog_in_channels
            except Exception as e:
                self.logger.error(f"Can not read the AnalogIn Channel Count. {e}")
                raise Exception(f"Can not read the AnalogIn Channel Count. {e}")
        else:
            self.logger.error(f"Can not read the AnalogIn Channel Count. Device not connected.")
            raise Exception(f"Can not read the AnalogIn Channel Count. Device not connected.")

    @mpPy6.CProcess.register_signal('_changed')
    def analog_in_bits(self) -> int:
        """
        Retrieves the number bits used by the AnalogIn ADC. The oscilloscope channel settings are identical
        across all channels.
        Calls WaveForms API Function 'FDwfAnalogInBitsInfo(HDWF hdwf, int *pnBits)'
        :return: The number bits used by the AnalogIn ADC.
        """
        int0 = c_int()
        if self.connected():
            self.dwf.FDwfAnalogInBitsInfo(self.hdwf, byref(int0))
            _adc_bits = int(int0.value)
            return _adc_bits
        else:
            self.logger.error(f"Can not read the AnalogIn Bits. Device not connected.")
            raise Exception(f"Can not read the AnalogIn Bits. Device not connected.")

    @mpPy6.CProcess.register_signal('_changed')
    def analog_in_buffer_size(self) -> tuple:
        """
        Returns the minimum and maximum allowable buffer sizes for the instrument. The oscilloscope
        channel settings are identical across all channels.
        Calls WaveForms API Function 'FDwfAnalogInBufferSizeInfo(HDWF hdwf, int *pnSizeMin, int *pnSizeMax)'
        :return: The minimum and maximum allowable buffer sizes for the instrument as a tuple (min, max).
        """
        if self.connected():
            int0 = c_int()
            int1 = c_int()
            self.dwf.FDwfAnalogInBufferSizeInfo(self.hdwf, byref(int0), byref(int1))
            _buffer_size = (int(int0.value), int(int0.value))
            return _buffer_size
        else:
            self.logger.error(f"Can not read the AnalogIn Buffer Size. Device not connected.")
            raise Exception(f"Can not read the AnalogIn Buffer Size. Device not connected.")

    @mpPy6.CProcess.register_signal('_changed')
    def analog_in_channel_range_info(self) -> tuple:
        """
        Returns the minimum and maximum range, peak to peak values, and the number of adjustable steps.
        The oscilloscope channel settings are identical across all channels.
        Calls WaveForms API Function
        'FDwfAnalogInChannelRangeInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps)'
        :return: The minimum and maximum range, peak to peak values, and the number of adjustable steps as a tuple
        (min, max, steps).
        """
        if self.connected:
            dbl0 = c_double()
            dbl1 = c_double()
            dbl2 = c_double()
            self.dwf.FDwfAnalogInChannelRangeInfo(self.hdwf, byref(dbl0), byref(dbl1), byref(dbl2))
            _range = (int(dbl0.value), int(dbl1.value), int(dbl2.value))
            return _range
        else:
            self.logger.error(f"Can not read the AnalogIn Channel Range. Device not connected.")
            raise Exception(f"Can not read the AnalogIn Channel Range. Device not connected.")

    @mpPy6.CProcess.register_signal('_changed')
    def analog_in_offset(self) -> tuple:
        """ Returns the minimum and maximum offset levels supported, and the number of adjustable steps"""
        if self.connected():
            dbl0 = c_double()
            dbl1 = c_double()
            dbl2 = c_double()
            self.dwf.FDwfAnalogInChannelOffsetInfo(self.hdwf, byref(dbl0), byref(dbl1), byref(dbl2))
            _offset = (int(dbl0.value), int(dbl1.value), int(dbl2.value))
            return _offset
        else:
            self.logger.error(f"Can not read the AnalogIn Offset. Device not connected.")
            raise Exception(f"Can not read the AnalogIn Offset. Device not connected.")

    # ==================================================================================================================
    # Function for setting up the acquisition
    # ==================================================================================================================
    def setup_acquisition(self, sample_rate: float, ain_channel: int):
        # self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1),
        #                            byref(self._ain_device_state))  # Variable to receive the acquisition state
        self.logger.info(f"[Task] Setup for acquisition on channel {ain_channel} with rate {sample_rate} Hz.")
        self.dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(ain_channel), c_int(1))
        self.dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(ain_channel), c_double(5))
        self.dwf.FDwfAnalogInAcquisitionModeSet(self.hdwf, acqmodeRecord)
        self.dwf.FDwfAnalogInFrequencySet(self.hdwf, c_double(sample_rate))
        self.dwf.FDwfAnalogInRecordLengthSet(self.hdwf, c_double(0))  # -1 infinite record length
        self.dwf.FDwfAnalogInConfigure(self.hdwf, c_int(1), c_int(0))
        # Variable to receive the acquisition state
        # self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(self._ain_device_state))
        self.logger.info(f"[Task] Wait 2 seconds for the offset to stabilize.")
        # wait at least 2 seconds for the offset to stabilize
        time.sleep(2)
        self.logger.info(f"[Task] Setup for acquisition done.")

    # ==================================================================================================================
    # Python wrapper for WaveForms API Functions
    # ==================================================================================================================
    @timeit
    def _dwf_analog_in_status(self, hdwf, read_data, ptr_device_state):
        try:
            _read_data_cint = c_int(int(read_data))
            self.dwf.FDwfAnalogInStatus(hdwf, _read_data_cint, ptr_device_state)
        except Exception as e:
            self.logger.error(f"Error while getting data from device: {e}")
            raise Exception(f"Error while getting data from device: {e}")
        return ptr_device_state

    @timeit
    def _dwf_analog_in_status_record(self, hdwf, ptr_c_available, ptr_c_lost, ptr_c_corrupted):
        """
        Retrieves information about the recording process. The data loss occurs when the device acquisition
        is faster than the read process to PC. In this case, the device recording buffer is filled and data
        samples are overwritten. Corrupt samples indicate that the samples have been overwritten by the
        acquisition process during the previous read.
        :param hdwf: Interface handle
        :param c_available: Pointer to variable to receive the available number of samples.
        :param c_lost: Pointer to variable to receive the lost samples after the last check.
        :param c_corrupted:Pointer to variable to receive the number of samples that could be corrupt.
        :return:
        """
        try:
            self.dwf.FDwfAnalogInStatusRecord(hdwf, ptr_c_available, ptr_c_lost, ptr_c_corrupted)
        except Exception as e:
            self.logger.error(f"Error while getting data from device: {e}")
            raise Exception(f"Error while getting data from device: {e}")
        return ptr_c_available, ptr_c_lost, ptr_c_corrupted

    @timeit
    def _dwf_analog_in_status_data(self, hdwf, channel, ptr_rgd_samples, c_available):
        """
        Retrieves the acquired data samples from the specified idxChannel on the AnalogIn instrument. It
        copies the data samples to the provided buffer.
        :param hdwf: Interface handle
        :param channel: Channel index
        :param rgd_samples: Pointer to allocated buffer to copy the acquisition data.
        :return:
        """
        try:
            self.dwf.FDwfAnalogInStatusData(hdwf, c_int(channel), ptr_rgd_samples, c_available)  # get channel data
        except Exception as e:
            self.logger.error(f"Error while getting data from device: {e}")
            raise Exception(f"Error while getting data from device: {e}")
        return ptr_rgd_samples, c_available

    @mpPy6.CProcess.register_signal(signal_name='device_state_changed')
    def device_state(self, state):
        return state

    @mpPy6.CProcess.register_signal(signal_name='capture_process_state_changed')
    def capture_process_state(self, state):
        return state

    # ==================================================================================================================
    #
    # ==================================================================================================================
    @mpPy6.CProcess.register_signal()
    def start_capturing_process(self):
        """
        Captures data from the device and puts it into a queue.
        :param ain_channel:
        :param sample_rate:
        :return: None
        """
        self.logger.info(f"Starting capture on channel {self.selected_ain_channel} with rate {self.sample_rate} Hz.")
        hdwf = self.hdwf
        self.device_state(AD2Constants.DeviceState.DEV_CAPT_SETUP())

        self.setup_sine_wave(self.selected_ain_channel)

        self.setup_acquisition(self.sample_rate, self.selected_ain_channel)

        # Variable to receive the acquisition state
        # self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(self._ain_device_state))
        # self.logger.info(f"[Task] Wait 2 seconds for the offset to stabilize.")
        # wait at least 2 seconds for the offset to stabilize
        time.sleep(2)
        # self.logger.info(f"[Task] Setup for acquisition done.")

        # Creates a Sin Wave on the Analog Out Channel 0

        # self.logger.info("Configuring acquisition. Starting oscilloscope.")

        # Configures the instrument and start or stop the acquisition. To reset the Auto trigger timeout, set
        self.dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))
        # self.logger.info("Device configured. Starting acquisition.")

        time_capture_started = 0
        capture_samples = 0
        capture_started = False
        capture_ended = False

        cAvailable = c_int()
        cLost = c_int()
        cCorrupted = c_int()
        cSamples = 0
        sts = c_byte()

        try:
            # self.dwf.FDwfAnalogOutReset(self.hdwf, c_int(0))
            self.device_state(AD2Constants.DeviceState.DEV_CAPT_STREAMING())
            self.ready_for_recording = True
            while self.kill_capture_flag.value == int(False) and self._kill_flag.value == int(True):
                self.dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
                # self._c_samples = 0

                time_start = time.time()

                # Checks the state of the acquisition. To read the data from the device, set fReadData to TRUE. For
                # single acquisition mode, the data will be read only when the acquisition is finished
                if sts == DwfStateConfig or sts == DwfStatePrefill or sts == DwfStateArmed:
                    # self.device_state(AD2Constants.DeviceState.ACQ_NOT_STARTED())
                    continue  # Acquisition not yet started.

                self.dwf.FDwfAnalogInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
                if cAvailable.value == 0:
                    # self.device_state(AD2Constants.DeviceState.NO_SAMPLES_AVAILABLE())
                    continue

                rgd_samples = (c_double * cAvailable.value)()
                # Get the data from the device and store it in rgd_samples
                self.dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(rgd_samples), cAvailable)

                arr = np.array(rgd_samples, copy=True)
                iteration_time = time.time() - time_start

                if self.start_capture_flag.value == int(True):
                    if not capture_started:
                        self.capture_process_state(AD2Constants.CapturingState.RUNNING())
                        self.logger.info(
                            "**************************** START command received. Acquisition started.")
                        time_capture_started = time.time()
                        capture_started = True
                elif self.start_capture_flag.value == int(False) and capture_started:
                    capture_started = False
                    self.logger.info(
                        "**************************** STOP command received. Acquisition stopped.")
                    self.capture_process_state(AD2Constants.CapturingState.STOPPED())
                    time_capture_stopped = time.time()
                    time_captured = time_capture_stopped - time_capture_started
                    self.logger.info(
                        f"Acquisition stopped after {time_captured} seconds "
                        f"samples. Resulting in a time of {capture_samples / self.sample_rate} s.")
                self.stream_data_queue.put(arr)

        except Exception as e:
            self.logger.error(f"Error while capturing data from device: {e}")
            raise Exception(f"Error while capturing data from device: {e}")
        self.logger.info("Capture thread ended.")
        self.ready_for_recording = False
        self.close_device()

    # ==================================================================================================================
    # Others
    # ==================================================================================================================
    def setup_sine_wave(self, channel: int = 0, amplitude: float = 1, frequency: float = 1):
        self.logger.debug("Generating AM sine wave...")
        self.dwf.FDwfAnalogOutNodeEnableSet(self.hdwf, c_int(channel), c_int(0), c_int(1))  # carrier
        self.dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf, c_int(channel), c_int(0), c_int(1))  # sine
        self.dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, c_int(channel), c_int(0), c_double(frequency))
        self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, c_int(channel), c_int(0), c_double(amplitude))
        # dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), c_int(0), c_double(0.5))
        # dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(2), c_int(1))  # AM
        # dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), c_int(2), c_int(3))  # triangle
        # dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), c_int(2), c_double(0.1))
        # dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), c_int(2), c_double(50))
        self.dwf.FDwfAnalogOutConfigure(self.hdwf, c_int(channel), c_int(1))
        time.sleep(1)
        self.logger.debug(f"Sine wave on output channel {channel} configured.")


if __name__ == "__main__":
    state_queue = Queue()
    cmd_queue = Queue()

    streaming_data_queue = Queue()
    start_capture_flag = Value('i', 0)
    kill_capture_flag = Value('i', 0)

    mpcapt = MPCaptDevice(state_queue, cmd_queue,
                          streaming_data_queue,
                          start_capture_flag,
                          kill_capture_flag, False
                          )
    mpcapt.logger, _ = mpcapt.create_new_logger("MPCaptDevice")
    mpcapt.start_capture(1000, 0)
