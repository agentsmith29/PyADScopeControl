#!/.venv/Scripts/python

from ctypes import c_int, byref, create_string_buffer, cdll, c_int32, c_uint, c_double

from CaptDeviceControl.controller.BaseAD2CaptDevice import BaseAD2CaptDevice
from CaptDeviceControl.model.AD2CaptDeviceModel import AD2CaptDeviceModel
#from .controller.BaseAD2CaptDevice import BaseAD2CaptDevice
#from .model.AD2CaptDeviceModel import AD2CaptDeviceModel

from CaptDeviceControl.constants.dwfconstants import enumfilterUSB, enumfilterType, enumfilterDemo
from CaptDeviceControl.controller.mp_AD2Capture.MPCaptDeviceControl import MPCaptDeviceControl


class AD2CaptDeviceController(BaseAD2CaptDevice):

    def __init__(self, ad2capt_model: AD2CaptDeviceModel):
        self.dwf = cdll.dwf
        super().__init__(ad2capt_model)



        # This is required for acquiring the data



    def read_hardware_config(self, iDevice):
        hw_info_dict = {}
        hdwf = c_int()
        int0 = c_int()
        int1 = c_int()
        uint0 = c_uint()
        dbl0 = c_double()
        dbl1 = c_double()
        dbl2 = c_double()
        self.dwf.FDwfDeviceConfigOpen(c_int(iDevice), c_int(0), byref(hdwf))
        if hdwf.value == 0:
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            raise Exception(str(szerr.value))

        self.dwf.FDwfAnalogInChannelCount(hdwf, byref(int0))
        hw_info_dict["analog_in_channels"] = int(int0.value)

        self.dwf.FDwfAnalogIOChannelCount(hdwf, byref(int0))
        hw_info_dict["analog_io_channels"] = int(int0.value)

        self.dwf.FDwfAnalogInBufferSizeInfo(hdwf, 0, byref(int0))
        hw_info_dict["buffer_size"] = int(int0.value)

        self.dwf.FDwfAnalogInBitsInfo(hdwf, byref(int0))
        hw_info_dict["adc_bits"] = int(int0.value)

        self.dwf.FDwfAnalogInChannelRangeInfo(hdwf, byref(dbl0), byref(dbl1), byref(dbl2))
        hw_info_dict["range"] = (int(dbl0.value), int(dbl1.value), int(dbl2.value))

        self.dwf.FDwfAnalogInChannelOffsetInfo(hdwf, byref(dbl0), byref(dbl1), byref(dbl2))
        hw_info_dict["offset"] = (int(dbl0.value), int(dbl1.value), int(dbl2.value))

        return hw_info_dict


    def discover_connected_devices(self):
        pass
        #self.mpcaptdevicecontrol.discover_connected_devices()



    # def _open_device(self, device_index):
    #     devicename = create_string_buffer(64)
    #     serialnum = create_string_buffer(16)
    #
    #     self.dwf.FDwfEnumDeviceName(c_int(device_index), devicename)
    #     self.dwf.FDwfEnumSN(c_int(device_index), serialnum)
    #
    #     self.model.device_name = devicename
    #     self.model.device_serial_number = serialnum
    #     # open device
    #     self.logger.info(f"[{self.pref} Task] Opening device #{device_index}...")
    #
    #     # Opens a device identified by the enumeration index and retrieves a handle. To automatically
    #     # enumerate all connected devices and open the first discovered device, use index -1.
    #     self.dwf.FDwfDeviceOpen(c_int(device_index), byref(self.model.hdwf))
    #
    #     if self.model.hdwf.value == hdwfNone.value:
    #         szerr = create_string_buffer(512)
    #         self.dwf.FDwfGetLastErrorMsg(szerr)
    #         # print(str(szerr.value))
    #         self.model.connected = False
    #         raise Exception(f"Failed to open device: {szerr.value}")
    #     else:
    #         self.model.connected = True
    #     self.get_analog_in_status()
    #     self.logger.info(f"[{self.pref} Task] Device connected!")
    #
    # def _setup_acquisition(self):
    #     # set up acquisition
    #     self.get_analog_in_status()
    #     self.logger.debug(f"[{self.pref} Task] Setup for acquisition. Wait 2 seconds for the offset to stabilize.")
    #     self.dwf.FDwfAnalogInChannelEnableSet(self.model.hdwf, c_int(self.model.analog_in_channel), c_int(1))
    #     self.dwf.FDwfAnalogInChannelRangeSet(self.model.hdwf, c_int(self.model.analog_in_channel), c_double(5))
    #     self.dwf.FDwfAnalogInAcquisitionModeSet(self.model.hdwf, acqmodeRecord)
    #     self.dwf.FDwfAnalogInFrequencySet(self.model.hdwf, c_double(self.model.hz_acquisition))
    #     self.dwf.FDwfAnalogInRecordLengthSet(self.model.hdwf, 0)  # -1 infinite record length
    #     self.get_analog_in_status()
    #     # wait at least 2 seconds for the offset to stabilize
    #     time.sleep(2)
    #     self.logger.info(f"[{self.pref} Task] Setup for acquisition done.")
    #     return True
    #
    # # # ==================================================================================================================
    # # #   Acquisition
    # # # ==================================================================================================================
    # # @Slot()
    # # def start_capture(self, capture):
    # #     if not self.model.connected:
    # #         self.logger.warning(f"[{self.pref} Task] No device connected. Connecting to first device.")
    # #         self.connect_device(0)
    # #         return False
    # #
    # #     if capture:
    # #         self.logger.info(f"[{self.pref} Task] Setting up device for capturing.")
    # #         self.gen_sine()
    # #         self._setup_acquisition()
    # #         # if self._setup_acquisition():
    # #         #    self.logger.info(f"[{self.pref} Task] Started capturing thread")
    # #         self.set_ad2_acq_status(True)
    # #         return self.thread_manager.start(self._capture)
    # #     else:
    # #         self.set_ad2_acq_status(False)
    # #     # return self._capture()
    # #
    # # def _capture(self):
    # #     self.model.capturing_finished = False
    # #     self.model.device_capturing = False
    # #     cAvailable = c_int()
    # #     cLost = c_int()
    # #     cCorrupted = c_int()
    # #
    # #     self.logger.info(f"[{self.pref} Report] Capturing started. "
    # #                      f"Waiting for start command: "
    # #                      f"{self.model.start_recording}<->{self.model.stop_recording}")
    # #
    # #     # Configures the instrument and start or stop the acquisition. To reset the Auto trigger timeout, set
    # #     # fReconfigure to TRUE.
    # #     # print("Starting oscilloscope")
    # #     self.dwf.FDwfAnalogInConfigure(self.model.hdwf, c_int(0), c_int(1))
    # #
    # #     t0 = -1
    # #
    # #     cSamples = 0
    # #     self.model.device_ready = True
    # #     self.logger.info(f"[{self.pref} Report] Capturing device is ready.")
    # #     while True:
    # #
    # #         if self.model.start_recording and not self.model.stop_recording:
    # #             if t0 < 0:
    # #                 self.logger.info(f"[{self.pref} Report] Start command received.")
    # #                 self.model.capturing_finished = False
    # #                 self.model.device_capturing = True
    # #                 self.model.current_recorded_samples = []
    # #                 timestamp = datetime.now()
    # #                 t0 = time.time()
    # #             # print(f"Start ({cSamples})")
    # #             sts = self.get_analog_in_status()
    # #
    # #             if cSamples == 0 and (
    # #                     sts == DwfStateConfig or
    # #                     sts == DwfStatePrefill or
    # #                     sts == DwfStateArmed):
    # #                 print('idle')
    # #                 continue  # Acquisition not yet started.
    # #
    # #             # Retrieves information about the recording process. The data loss occurs when the device acquisition
    # #             # is faster than the read process to PC. In this case, the device recording buffer is filled and data
    # #             # samples are overwritten. Corrupt samples indicate that the samples have been overwritten by the
    # #             # acquisition process during the previous read. In this case, try optimizing the loop process for faster
    # #             # execution or reduce the acquisition frequency or record length to be less than or equal to the device
    # #             # buffer size (record length <= buffer size/frequency).
    # #             self.dwf.FDwfAnalogInStatusRecord(self.model.hdwf,  # Interface handle
    # #                                               byref(cAvailable),
    # #                                               byref(cLost),
    # #                                               byref(cCorrupted))
    # #
    # #             cSamples += cLost.value
    # #
    # #             if cLost.value:
    # #                 self.logger.warning(f"[{self.pref} Report] - Sample(s) lost ({cLost.value})")
    # #                 self.model.fLost += int(cLost.value)
    # #             if cCorrupted.value:
    # #                 self.logger.warning(f"[{self.pref} Report] - Samples(s) corrupted ({cCorrupted.value})")
    # #                 self.model.fCorrupted += int(cCorrupted.value)
    # #
    # #             # self.dwf.FDwfAnalogInStatusSamplesValid(self.hdwf, byref(self.cValid))
    # #             if cAvailable.value == 0:
    # #                 # print(f"Nothing available {cAvailable.value}")
    # #                 continue
    # #             else:
    # #                 # print(f"Available: {cAvailable.value}")
    # #
    # #                 # if cSamples + cAvailable.value > self.ad2capt_model.n_samples:
    # #                 #    cAvailable = c_int(self.ad2capt_model.n_samples - cSamples)
    # #                 rgdSamples = (c_double * cAvailable.value)()
    # #                 # Retrieves the acquired data samples from the specified idxChannel on the AnalogIn instrument. It
    # #                 # copies the data samples to the provided buffer.
    # #                 self.dwf.FDwfAnalogInStatusData(self.model.hdwf,
    # #                                                 c_int(self.model.analog_in_channel),
    # #                                                 byref(rgdSamples),
    # #                                                 cAvailable)  # get channel 1 data
    # #                 for s in rgdSamples:
    # #                     self.model.current_recorded_samples.append(float(s))
    # #
    # #                 cSamples += cAvailable.value
    # #
    # #         elif not self.model.start_recording and self.model.stop_recording:
    # #             t1 = time.time()
    # #             self.model.measurement_time = t1 - t0
    # #             self.get_analog_in_status()
    # #             self.model.capturing_finished = True
    # #             self.model.device_capturing = False
    # #             self.logger.info(f"Finished Thread. Acquisition took {self.model.measurement_time} s. "
    # #                              f"Process captured {len(self.model.current_recorded_samples)} samples.")
    # #             # 1. Assign the current captured samples to a dict
    # #             self.model.all_recorded_samples.append({'timestamp': timestamp,
    # #                                                     'measurement_time': self.model.measurement_time,
    # #                                                     'num_samples': len(
    # #                                                         self.model.current_recorded_samples),
    # #                                                     'acqRate': self.model.hz_acquisition,
    # #                                                     'samples': self.model.current_recorded_samples})
    # #             # Reset status bits
    # #             try:
    # #                 time.sleep(1)
    # #                 self.close_device()
    # #             except Exception as e:
    # #                 print(e)
    # #             return
    # #             # return self.model.current_recorded_samples, self.model.measurement_time
    # #         else:
    # #             self.model.device_capturing = False
    #
    # # # ==================================================================================================================
    # # #
    # # # ==================================================================================================================
    # # def gen_sine(self, channel=0, frequency=1):
    # #     self.logger.debug(f"[{self.pref} Task] Generating sine wave on output 0...")
    # #     self.dwf.FDwfAnalogOutNodeEnableSet(self.model.hdwf, c_int(channel), AnalogOutNodeCarrier, c_int(1))
    # #     self.dwf.FDwfAnalogOutNodeFunctionSet(self.model.hdwf, c_int(channel), AnalogOutNodeCarrier,
    # #                                           funcTrapezium)  # sine
    # #     self.dwf.FDwfAnalogOutNodeFrequencySet(self.model.hdwf, c_int(channel), AnalogOutNodeCarrier,
    # #                                            c_double(frequency))  # 1Hz
    # #     self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.model.hdwf, c_int(channel), AnalogOutNodeCarrier, c_double(2))
    # #     self.dwf.FDwfAnalogOutConfigure(self.model.hdwf, c_int(channel), c_int(1))
    # #     return self.model.hdwf
    #
    # # ==================================================================================================================
    # #
    # # ==================================================================================================================
    # def close_device(self):
    #     # Resets and configures (by default, having auto configure enabled) all AnalogOut instrument
    #     # parameters to default values for the specified channel. To reset instrument parameters across all
    #     # channels, set idxChannel to -1.
    #     self.model.fLost = 0
    #     self.model.fCorrupted = 0
    #     self.model.start_recording = True
    #     self.model.stop_recording = False
    #     self.model.capturing_finished = False
    #     self.model.device_capturing = False
    #     self.model.connected = False
    #     self.model.device_state = 0
    #     self.model.dwf_version = "Unknown"
    #     self.model.device_serial_number = "Unknown"
    #     self.model.device_name = "Unknown"
    #     self.model.analog_in_channel = -1
    #
    #     self.dwf.FDwfAnalogOutReset(self.model.hdwf, c_int(self.model.analog_in_channel))
    #     self.dwf.FDwfDeviceCloseAll()
    #     self.logger.info(f"[{self.pref} Task] Device closed.")

    # def get_analog_in_status(self):
    #     sts: c_byte = c_byte()
    #     # Checks the state of the acquisition. To read the data from the device, set fReadData to TRUE. For
    #     # single acquisition mode, the data will be read only when the acquisition is finished.
    #     self.dwf.FDwfAnalogInStatus(self.model.hdwf,  # Interface handle.
    #                                 c_int(1),  # True, if data should be read
    #                                 byref(sts))  # Variable to receive the acquisition state
    #     self.model.device_state = sts.value
    #     return sts

    # ==================================================================================================================
    #
    # ==================================================================================================================
