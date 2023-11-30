import ctypes
import os
import sys
import time
from ctypes import c_int, c_int32, byref, create_string_buffer, cdll, c_double, c_byte, CDLL
from multiprocessing import Queue, Value

import cmp
import numpy as np

from constants.dwfconstants import enumfilterType, enumfilterDemo, enumfilterUSB, acqmodeRecord, DwfStateConfig, \
    DwfStatePrefill, DwfStateArmed


class MPCaptDevice(cmp.CProcess):
    @staticmethod
    def timeit(func):
        def wrapper(self, *args, **kwargs):
            time_start = time.time()
            res = func(self, *args, **kwargs)
            time_stop = time.time()
            print(f"Function {func.__name__} took {time_stop - time_start} seconds.")
            return res #time_stop - time_start

        return wrapper

    def __init__(self, state_queue, cmd_queue,
                 streaming_data_queue: Queue, capture_data_queue: Queue,
                 start_capture_flag: Value,
                 kill_capture_flag: Value,
                 enable_internal_logging):
        super().__init__(state_queue, cmd_queue, enable_internal_logging=enable_internal_logging)

        self._c_samples = None
        self._c_corrupted = None
        self._c_lost = None
        self._c_available = None

        self.start_capture_flag: Value = start_capture_flag
        self.kill_capture_flag: Value = kill_capture_flag

        self.stream_data_queue = streaming_data_queue
        self.capture_data_queue = capture_data_queue

        self.logger, self.ha = None, None

        self.dwf = None
        self.hdwf = None

        # Capture data counters

        self._dwf_version = None
        self._device_serial_number: str = ""
        self._device_name: str = ""
        self._connected = False

        self._samples_lost = 0
        self._samples_corrupted = 0

    def postrun_init(self):
        self.logger, self.ha = self.create_new_logger(f"{self.__class__.__name__}/({os.getpid()})")

        if sys.platform.startswith("win"):
            self.dwf = cdll.dwf
        elif sys.platform.startswith("darwin"):
            self.dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            self.dwf = cdll.LoadLibrary("libdwf.so")
        self._connected = self.connected()
        self.hdwf = c_int()
        self._ain_device_state: c_byte = c_byte()

        self._c_available = c_int()
        self._c_lost = c_int()
        self._c_corrupted = c_int()
        self._c_samples = 0

    @cmp.CProcess.register_for_signal('_changed')
    def device_capturing(self, capturing: bool):
        self.logger.info(f"Device capturing: {capturing}")
        return capturing

    @cmp.CProcess.register_for_signal('_changed')
    def dwf_version(self):
        self.logger.debug(f"Getting DWF version information...")
        version = create_string_buffer(16)
        self.dwf.FDwfGetVersion(version)
        return version.value.decode("utf-8")

    # ==================================================================================================================
    # Device Enumeration without connecting to the device
    # ==================================================================================================================
    @cmp.CProcess.register_for_signal('_changed')
    def connected_devices(self):
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
        filter, type = (c_int32(enumfilterType.value | enumfilterDemo.value | enumfilterUSB.value), 'USB')
        # filter, type = (c_int32(enumfilterType.value | enumfilterDemo.value), 'DEMO')
        self.logger.debug(f"Filtering {type} devices...")
        self.dwf.FDwfEnum(filter, byref(cDevice))
        num_of_connected_devices = cDevice
        self.logger.debug(f"Found {cDevice.value} {type} devices.")

        for iDevice in range(0, cDevice.value):
            connected_devices.append({
                'type': type,
                'device_id': int(iDevice),
                'device_name': self.device_name(iDevice),
                'serial_number': self.device_serial_number(iDevice)
            })
            # _mp_log_debug(f"Found {type} device: {devicename.value.decode('UTF-8')} ({serialnum.value.decode('UTF-8')})")
        # print(connected_devices)
        # print(f"Discoverd {len(self.model.connected_devices)} devices.")
        self.logger.info(f"Found {len(connected_devices)} devices.")
        return connected_devices

    @cmp.CProcess.register_for_signal('_changed')
    def ain_channels(self, device_id) -> list:
        cInfo = c_int()
        self.dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(1), byref(cInfo))
        ain_channels = cInfo.value
        if ain_channels == 0:
            # Sometimes, the device reports a wrong number of ain channels
            # so we can try to connect to the device first and retrieve the information
            self.open_device(device_id)
            ain_channels = self.analog_in_channels_count()
            self.close_device()
        self.logger.debug(f"Device {device_id} has {ain_channels} analog input channels.")
        return list(range(0, ain_channels))

    @cmp.CProcess.register_for_signal('_changed')
    def ain_buffer_size(self, device_id) -> int:
        cInfo = c_int()
        self.dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(7), byref(cInfo))
        return cInfo.value

    @cmp.CProcess.register_for_signal('_changed')
    def device_name(self, device_index: int) -> str:
        try:
            devicename = create_string_buffer(64)
            self.dwf.FDwfEnumDeviceName(c_int(device_index), devicename)
            return str(devicename.value.decode("utf-8"))
        except Exception as e:
            self.logger.error(f"Error while reading device name: {e}")
            raise Exception(f"Error while reading device name: {e}")

    @cmp.CProcess.register_for_signal('_changed')
    def device_serial_number(self, device_index: int) -> str:
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
    @cmp.CProcess.register_for_signal('_changed')
    def connected(self) -> bool:
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
        if self.connected():
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

    @cmp.CProcess.register_for_signal('_changed')
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

    @cmp.CProcess.register_for_signal('_changed')
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

    @cmp.CProcess.register_for_signal('_changed')
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

    @cmp.CProcess.register_for_signal('_changed')
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
    # Functions for opening and closing the device
    # ==================================================================================================================
    @cmp.CProcess.register_for_signal()
    def open_device(self, device_index):
        """
        Opens the device and returns the handle.
        :return: Device handle.
        """
        self.logger.debug(f"Opening device {device_index}...")
        self._dwf_version = self.dwf_version()

        # Opens the device specified by idxDevice. The device handle is returned in hdwf. If idxDevice is -1, the
        # first available device is opened.
        self.dwf.FDwfDeviceOpen(c_int(device_index), byref(self.hdwf))

        self._device_name = self.device_name(device_index)
        self._device_serial_number = self.device_serial_number(device_index)

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
        self._connected = self.connected()

    def close_device(self):
        # self.dwf.FDwfAnalogOutReset(self.hdwf, c_int(channel))
        self.logger.info(f"[Task] Closing device...")
        self.dwf.FDwfDeviceClose(self.hdwf)
        self.hdwf.value = 0
        self._connected = self.connected()
        self.logger.info(f"[Task] Device closed.")

    # ==================================================================================================================
    # Function for setting up the acquisition
    # ==================================================================================================================
    def setup_acquisition(self, sample_rate: float, ain_channel: int):
        self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1),
                                    byref(self._ain_device_state))  # Variable to receive the acquisition state
        self.logger.info(f"[Task] Setup for acquisition on channel {ain_channel} with rate {sample_rate} Hz.")
        self.dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(ain_channel), c_int(1))
        self.dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(ain_channel), c_double(5))
        self.dwf.FDwfAnalogInAcquisitionModeSet(self.hdwf, acqmodeRecord)
        self.dwf.FDwfAnalogInFrequencySet(self.hdwf, c_double(sample_rate))
        self.dwf.FDwfAnalogInRecordLengthSet(self.hdwf, 0)  # -1 infinite record length

        # Variable to receive the acquisition state
        #self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(self._ain_device_state))
        #self.logger.info(f"[Task] Wait 2 seconds for the offset to stabilize.")
        # wait at least 2 seconds for the offset to stabilize
        #time.sleep(2)
        #self.logger.info(f"[Task] Setup for acquisition done.")

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

    def start_capture(self, sample_rate: float, ain_channel: int):
        """
        Captures data from the device and puts it into a queue.
        :param ain_channel:
        :param sample_rate:
        :return: None
        """
        # FDwfAnalogInStatus(HDWF hdwf, BOOL fReadData, DwfState* psts)
        self.setup_acquisition(ain_channel=ain_channel, sample_rate=sample_rate)

        # Creates a Sin Wave on the Analog Out Channel 0
        self.setup_sine_wave(channel=0)
        self.logger.info("Configuring acquisition. Starting oscilloscope.")

        # Configures the instrument and start or stop the acquisition. To reset the Auto trigger timeout, set
        self.dwf.FDwfAnalogInConfigure(self.hdwf, c_int(0), c_int(1))
        self.logger.info("Device configured. Starting acquisition.")

        time_capture_started = 0
        capture_samples = 0
        capture_started = False
        capture_ended = False

        n_samples = int((sample_rate*2))
        rgd_samples = (c_double * n_samples)()
        #num_sent_samples = 0
        try:
            self.dwf.FDwfAnalogOutReset(self.hdwf, c_int(0))


            while self.kill_capture_flag.value == int(False):
                self._c_samples = 0


                time_start = time.time()

                # Checks the state of the acquisition. To read the data from the device, set fReadData to TRUE. For
                # single acquisition mode, the data will be read only when the acquisition is finished
                self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(self._ain_device_state))

                if self._c_samples == 0 and (
                        self._ain_device_state == DwfStateConfig or
                        self._ain_device_state == DwfStatePrefill or
                        self._ain_device_state == DwfStateArmed):
                    # self.logger.info("Device in idle state. Waiting for acquisition to start.")
                    continue  # Acquisition not yet started.

                self.dwf.FDwfAnalogInStatusRecord(self.hdwf,
                                                  byref(self._c_available),
                                                  byref(self._c_lost), byref(self._c_corrupted)
                                                  )
                self._c_samples += self._c_lost.value
                #if self._c_lost.value:
                #    self._samples_lost += self._c_lost.value
                #if self._c_corrupted.value:
                #    self._samples_corrupted += self._c_corrupted.value

                # self.dwf.FDwfAnalogInStatusSamplesValid(self.hdwf, byref(self.cValid))
                if self._c_available.value == 0:
                    pass
                    #print("Nothing available")
                    #continue

                else:
                    if self._c_samples + self._c_available.value > n_samples:
                        self._c_available = c_int(n_samples - self._c_samples)

                    # print(f"Available: {self._c_available.value}")
                    # if cSamples + cAvailable.value > self.ad2capt_model.n_samples:
                    #    cAvailable = c_int(self.ad2capt_model.n_samples - cSamples)
                    # time_rgdsamples_start = time.time()

                    # arr = [None] * cAvailable.value
                    # time_rgdsamples_stop = time.time()
                    # time_rgdsamples = time_rgdsamples_stop - time_rgdsamples_start
                    # print(f"rgd_samples took {time_rgdsamples} seconds")
                    rgd_samples = (c_double * self._c_available.value)()
                    # Get the data from the device and store it in rgd_samples
                    self.dwf.FDwfAnalogInStatusData(self.hdwf,
                                                    c_int(ain_channel),
                                                    rgd_samples,
                                                    self._c_available)
                    #print(f"Got data from device: {self._c_available.value}")
                    self._c_samples += self._c_available.value
                    iteration_time = time.time() - time_start

                # Convert the data to a numpy array and put it into the queue
                # self.logger.info("Convert data to numpy array and put it into the queue.")

                #    num_sent_samples = 0
                arr = np.array(rgd_samples)
                #print(f"I send {len(arr)} samples to the queue.")
                self.stream_data_queue.put(arr)

                if self.start_capture_flag.value == int(True):
                    if not capture_started:
                        self.device_capturing(True)
                        time_capture_started = time.time()
                        self.logger.info(
                            "**************************** Starting command received. Acquisition started.")
                        capture_started = True
                        capture_ended = False
                        capture_samples = 0
                    #capture_samples = capture_samples + len(arr)
                    #self.capture_data_queue.put(arr)
                elif self.start_capture_flag.value == int(False):

                    if not capture_ended and capture_started:
                        self.device_capturing(False)
                        time_capture_stopped = time.time()
                        time_captured = time_capture_stopped - time_capture_started
                        self.logger.info(
                            "**************************** Stopping command received. Acquisition stopped.")
                        self.logger.info(
                            f"Acquisition stopped after {time_captured} seconds. Captured {capture_samples} "
                            f"samples. Resulting in a time of {capture_samples / sample_rate} s.")
                        capture_ended = True
                        capture_started = False
                        #self.capture_data_queue.put(arr)
                # self._c_samples += self._c_available.value



        except Exception as e:
            self.logger.error(f"Error while capturing data from device: {e}")
            raise Exception(f"Error while capturing data from device: {e}")
        self.logger.info("Capture thread ended.")
        self.close_device()

    # ==================================================================================================================
    # Others
    # ==================================================================================================================
    def setup_sine_wave(self, channel: int = 0):
        self.logger.debug("Generating AM sine wave...")
        self.dwf.FDwfAnalogOutNodeEnableSet(self.hdwf, c_int(0), c_int(0), c_int(1))  # carrier
        self.dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf, c_int(0), c_int(0), c_int(1))  # sine
        self.dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, c_int(0), c_int(0), c_double(0.1))
        self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, c_int(0), c_int(0), c_double(1))
        # dwf.FDwfAnalogOutNodeOffsetSet(hdwf, c_int(0), c_int(0), c_double(0.5))
        # dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(2), c_int(1))  # AM
        # dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), c_int(2), c_int(3))  # triangle
        # dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), c_int(2), c_double(0.1))
        # dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), c_int(2), c_double(50))
        self.dwf.FDwfAnalogOutConfigure(self.hdwf, c_int(channel), c_int(1))
        time.sleep(1)
        self.logger.debug(f"Sine wave on output channel {channel} configured.")
