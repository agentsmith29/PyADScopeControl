import os
import sys
import time
from ctypes import c_int, c_int32, byref, create_string_buffer, cdll, c_double, c_byte
from multiprocessing import Queue, Value

import cmp

from constants.dwfconstants import enumfilterType, enumfilterDemo, enumfilterUSB, acqmodeRecord, DwfStateConfig, \
    DwfStatePrefill, DwfStateArmed


class MPCaptDevice(cmp.CProcess):
    def __init__(self, state_queue, cmd_queue,
                 streaming_data_queue: Queue,
                 capture_data_queue: Queue,
                 start_capture_flag: Value,
                 enable_logging):
        super().__init__(state_queue, cmd_queue, enable_logging=enable_logging)

        self.start_capture_flag: Value = start_capture_flag
        self.stream_data_queue = streaming_data_queue
        self.capture_data_queue = capture_data_queue

        self.logger, self.ha = None, None

        self.dwf = None
        self.hdwf = None

        self._dwf_version = None
        self._device_serial_number: str = ""
        self._device_name: str = "None"
        self._connected = self.connected()

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

        self.hdwf = c_int()
        self._ain_device_state: c_byte = c_byte()

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

        devicename = create_string_buffer(64)
        serialnum = create_string_buffer(16)

        for iDevice in range(0, cDevice.value):
            self.dwf.FDwfEnumDeviceName(c_int(iDevice), devicename)
            self.dwf.FDwfEnumSN(c_int(iDevice), serialnum)
            connected_devices.append({
                'type': type,
                'device_id': int(iDevice),
                'device_name': str(devicename.value.decode('UTF-8')),
                'serial_number': str(serialnum.value.decode('UTF-8'))
            })
            # _mp_log_debug(f"Found {type} device: {devicename.value.decode('UTF-8')} ({serialnum.value.decode('UTF-8')})")
        # print(connected_devices)
        # print(f"Discoverd {len(self.model.connected_devices)} devices.")
        return connected_devices

    @cmp.CProcess.register_for_signal('_changed')
    def ain_channels(self, device_id) -> list:
        print(f">>> Reading available analog input channels for device {device_id}.")
        cInfo = c_int()
        self.dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(1), byref(cInfo))
        return list(range(0, cInfo.value))

    @cmp.CProcess.register_for_signal('_changed')
    def ain_buffer_size(self, device_id) -> int:
        cInfo = c_int()
        self.dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(7), byref(cInfo))
        return cInfo.value

    @cmp.CProcess.register_for_signal('_changed')
    def dwf_version(self):
        self.logger.debug(f"Getting DWF version information...")
        version = create_string_buffer(16)
        self.dwf.FDwfGetVersion(version)
        return version.value.decode("utf-8")

    @cmp.CProcess.register_for_signal('_changed')
    def device_name(self, device_index: int) -> str:
        devicename = create_string_buffer(64)
        self.dwf.FDwfEnumDeviceName(c_int(device_index), devicename)
        return str(devicename.value.decode("utf-8"))

    @cmp.CProcess.register_for_signal('_changed')
    def device_serial_number(self, device_index: int) -> str:
        serialnum = create_string_buffer(16)
        self.dwf.FDwfEnumSN(c_int(device_index), serialnum)
        return str(serialnum.value.decode("utf-8")).replace("SN:", "")

    @cmp.CProcess.register_for_signal('_changed')
    def connected(self) -> bool:
        if self.hdwf is None or self.hdwf.value == 0:
            return False
        else:
            return True

    @cmp.CProcess.register_for_signal()
    def open_device(self, device_index):
        """
        Opens the device and returns the handle.
        :return: Device handle.
        """
        self._dwf_version = self.dwf_version()
        self._device_name = self.device_name(device_index)
        self._device_serial_number = self.device_serial_number(device_index)

        # Opens the device specified by idxDevice. The device handle is returned in hdwf. If idxDevice is -1, the
        # first available device is opened.
        self.logger.info(f"[Task] Opening device #{device_index}...")
        self.dwf.FDwfDeviceOpen(c_int(device_index), byref(self.hdwf))

        if self.hdwf.value == 0:
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            self.logger.error(f"Failed to open device: {szerr.value}")
            # ad2_state.connected = False
            raise Exception(f"Failed to open device: {szerr.value}")
        else:
            self.logger.info(f"Device opened: {self._device_name} "
                             f"({self._device_serial_number})")
        self._connected = self.connected()

    def close_device(self):
        #self.dwf.FDwfAnalogOutReset(self.hdwf, c_int(channel))
        self.logger.info(f"[Task] Closing device...")
        self.dwf.FDwfDeviceClose(self.hdwf)
        self.hdwf.value = 0
        self._connected = self.connected()
        self.logger.info(f"[Task] Device closed.")

    def setup_aquisition(self, sample_rate: float, ain_channel: int):
        self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1),
                               byref(self._ain_device_state))  # Variable to receive the acquisition state
        self.logger.info(f"[Task] Setup for acquisition on channel {ain_channel} with rate {sample_rate} Hz.")
        self.dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(ain_channel), c_int(1))
        self.dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(ain_channel), c_double(5))
        self.dwf.FDwfAnalogInAcquisitionModeSet(self.hdwf, acqmodeRecord)
        self.dwf.FDwfAnalogInFrequencySet(self.hdwf, c_double(sample_rate))
        self.dwf.FDwfAnalogInRecordLengthSet(self.hdwf, 0)  # -1 infinite record length

        # Variable to receive the acquisition state
        self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(self._ain_device_state))
        self.logger.info(f"[Task] Wait 2 seconds for the offset to stabilize.")
        # wait at least 2 seconds for the offset to stabilize
        time.sleep(2)
        self.logger.info(f"[Task] Setup for acquisition done.")

    def start_capture(self, sample_rate: float, ain_channel: int):
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
        # Streaming the data should only be set to 1000Hz, otherwise the UI will freeze. The capturing however should
        # stay at the given sample rate.
        # Using the modulo operation allow us to determine the variable stream_n that is required
        # to scale down the streaming rate.
        stream_rate = 1000  # Hz
        # stream_n = sample_rate / stream_rate
        # stream_sample_cnt = 0

        time_capture_started = 0
        capturing_notified = False
        # Print pid and ppid
        self.logger.info(f"Starting capture thread, pid={os.getpid()}")
        #ad2_state = AD2StateMPSetter(state_queue)

        #ad2_state.pid = os.getpid()

        #ad2_state.selected_ain_channel = channel
        #ad2_state.sample_rate = sample_rate
        #self.logger.debug(f"Setting up device {device_id} with "
        #              f"channel {ad2_state.selected_ain_channel} and "
        #              f"acquisition rate {ad2_state.sample_rate} Hz")

        #dwf, hdwf = _mp_open_device(device_id, ad2_state)

        # acquisition_state = c_byte()

        cAvailable = c_int()
        cLost = c_int()
        cCorrupted = c_int()

        # FDwfAnalogInStatus(HDWF hdwf, BOOL fReadData, DwfState* psts)
        self.setup_aquisition(ain_channel=ain_channel, sample_rate=sample_rate)
        #_t_setup_sine_wave(dwf, hdwf, ad2_state)

        self.logger.info("Configuring acquisition. Starting oscilloscope.")
        # FDwfAnalogInConfigure(HDWF hdwf, int fReconfigure, int fStart)
        # Configures the instrument and start or stop the acquisition. To reset the Auto trigger timeout, set
        # fReconfigure to TRUE.
        # hdwf – Interface handle.
        # fReconfigure – Configure the device.
        # fStart – Start the acquisition.
        self.dwf.FDwfAnalogInConfigure(self.hdwf, c_int(0), c_int(1))

        self.logger.info("Device configured. Starting acquisition.")

        cSamples = 0
        capture_samples = 0
        #print(end_process.value)
        # Checks the state of the acquisition. To read the data from the device, set fReadData to TRUE. For
        # single acquisition mode, the data will be read only when the acquisition is finished
        time_FDwfAnalogInStatus_start = time.time()
        self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(self._ain_device_state))
        time_FDwfAnalogInStatus_stop = time.time()
        time_FDwfAnalogInStatus = time_FDwfAnalogInStatus_stop - time_FDwfAnalogInStatus_start
        print(f"FDwfAnalogInStatus took {time_FDwfAnalogInStatus} seconds")

        while True:
            time_start = time.time()
            print("New iteration")



            time_cSamples_start = time.time()
            if cSamples == 0 and (
                    self._ain_device_state == DwfStateConfig or
                    self._ain_device_state == DwfStatePrefill or
                    self._ain_device_state == DwfStateArmed):
                self.logger.info("Device in idle state. Waiting for acquisition to start.")
                continue  # Acquisition not yet started.
            time_cSamples_stop = time.time()
            time_cSamples = time_cSamples_stop - time_cSamples_start
            print(f"cSamples took {time_cSamples} seconds")


            time_FDwfAnalogInStatusRecord_start = time.time()
            self.dwf.FDwfAnalogInStatusRecord(self.hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
            cSamples += cLost.value
            time_FDwfAnalogInStatusRecord_stop = time.time()
            time_FDwfAnalogInStatusRecord = time_FDwfAnalogInStatusRecord_stop - time_FDwfAnalogInStatusRecord_start
            print(f"FDwfAnalogInStatusRecord took {time_FDwfAnalogInStatusRecord} seconds")

            time_samples_l_c_start = time.time()
            if cLost.value:
                self._samples_lost += cLost.value
            if cCorrupted.value:
                self._samples_corrupted += cCorrupted.value
            time_samples_l_c_stop = time.time()
            time_samples_l_c = time_samples_l_c_stop - time_samples_l_c_start
            print(f"time_samples_l_c took {time_samples_l_c} seconds")

            # self.dwf.FDwfAnalogInStatusSamplesValid(self.hdwf, byref(self.cValid))
            if cAvailable.value == 0:
                print(cAvailable.value)
                continue
            else:
                # print(f"Available: {cAvailable.value}")
                # if cSamples + cAvailable.value > self.ad2capt_model.n_samples:
                #    cAvailable = c_int(self.ad2capt_model.n_samples - cSamples)
                time_rgdsamples_start = time.time()
                rgdSamples = (c_double * cAvailable.value)()
                time_rgdsamples_stop = time.time()
                time_rgdsamples = time_rgdsamples_stop - time_rgdsamples_start
                print(f"rgdSamples took {time_rgdsamples} seconds")

                time_FDwfAnalogInStatusData_start = time.time()
                self.dwf.FDwfAnalogInStatusData(self.hdwf, c_int(ain_channel), byref(rgdSamples), cAvailable)  # get channel data
                time_FDwfAnalogInStatusData_stop = time.time()
                time_FDwfAnalogInStatusData = time_FDwfAnalogInStatusData_stop - time_FDwfAnalogInStatusData_start
                print(f"FDwfAnalogInStatusData took {time_FDwfAnalogInStatusData} seconds")

                # Print how many samples are available
                status = {"available": cAvailable.value, 'captured': len(rgdSamples), 'lost': cLost.value,
                          'corrupted': cCorrupted.value, "time": time.time()}
                self.logger.debug(status)
                print(f"took: {time.time() - time_start} seconds")
                #self.stream_data_queue.put(
                #    ([(float(s)) for s in rgdSamples], status)
                #)

                # if self.start_capture.value == int(True):
                #     if not capturing_notified:
                #         time_capture_started = time.time()
                #         capture_samples = 0
                #         _mp_log_info("Starting command recieved. Acquisition started.")
                #         ad2_state.acquisition_state = AD2Constants.CapturingState.RUNNING()
                #         capturing_notified = True
                #     capture_samples = capture_samples + len(rgdSamples)
                #     status = {
                #         "available": cAvailable.value,
                #         "captured": capture_samples,
                #         "lost": cLost.value,
                #         "corrupted": cCorrupted.value,
                #         "recording_time": time.time() - time_capture_started}
                #     capture_data_queue.put(([float(s) for s in rgdSamples], status))
                #     # capture_data_queue.put([float(s) for s in rgdSamples])
                # elif start_capture.value == 0:
                #     if capturing_notified:
                #         ad2_state.acquisition_state = AD2Constants.CapturingState.STOPPED()
                #         time_capture_stopped = time.time()
                #         time_captured = time_capture_stopped - time_capture_started
                #         ad2_state.recording_time = time_captured
                #         _mp_log_info(f"Acquisition stopped after {time_captured} seconds. Captured {capture_samples} "
                #                      f"samples. Resulting in a time of {capture_samples / ad2_state.sample_rate} s.")
                #         status = {
                #             "available": cAvailable.value,
                #             "captured": capture_samples,
                #             "lost": cLost.value,
                #             "corrupted": cCorrupted.value,
                #             "recording_time": time.time() - time_capture_started}
                #         capture_data_queue.put(([float(s) for s in rgdSamples], status))
                #
                #         capturing_notified = False
                cSamples += cAvailable.value

        self.close_device()
