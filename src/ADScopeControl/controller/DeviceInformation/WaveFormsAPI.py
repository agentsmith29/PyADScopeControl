# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
import logging
import sys
from ctypes import c_int, byref, c_double, CDLL, create_string_buffer, cdll, c_int32

from ADScopeControl.constants.dwfconstants import enumfilterType, enumfilterDemo, enumfilterUSB


class WFAPI:

    @staticmethod
    def _check_device_connection(dwf: CDLL, hwdf: c_int):
        if hwdf.value == 0:
            szerr = create_string_buffer(512)
            dwf.FDwfGetLastErrorMsg(szerr)
            raise Exception(str(szerr.value))


class WFAPIChannels(WFAPI):

    def __init__(self):
        super().__init__()

    @staticmethod
    def analog_in_channels_count(dwf: CDLL, hdwf: c_int) -> int:
        """
        Reads the number of AnalogIn channels of the device. The oscilloscope channel settings are
        identical across all channels.
        Calls WaveForms API Function 'FDwfAnalogInChannelCount(HDWF hdwf, int *pcChannel)'
        :return: The number of analog in channels.
        """
        WFAPI._check_device_connection(dwf, hdwf)
        int0 = c_int()
        dwf.FDwfAnalogInChannelCount(hdwf, byref(int0))
        _analog_in_channels = int(int0.value)
        return _analog_in_channels

    @staticmethod
    def analog_on_channel_enable_set(dwf: CDLL, hdwf: c_int, channel: int, enable: bool):
        """
        Not implemented.
        Enables or disables the specified AnalogIn channel.
        Calls WaveForms API Function 'FDwfAnalogInChannelEnableSet(HDWF hdwf, int idxChannel, int fEnable)'
        :param channel: The channel to enable or disable.
        :param enable: True to enable the channel, False to disable it.
        """
        WFAPI._check_device_connection(dwf, hdwf)
        raise NotImplementedError()

    @staticmethod
    def analog_in_channel_enable_get(dwf: CDLL, hdwf: c_int, channel: int) -> bool:
        """
        Not implemented.
        Gets the current enable/disable status of the specified AnalogIn channel.
        Calls WaveForms API Function 'FDwfAnalogInChannelEnableGet(HDWF hdwf, int idxChannel, int *pfEnable)'
        :param channel: Index of channel to get the enable/disable status of.
        """
        WFAPI._check_device_connection(dwf, hdwf)
        raise NotImplementedError()

    @staticmethod
    def analog_in_channel_filter_info(dwf: CDLL, hdwf: c_int, filter_number: int):
        """
        Not implemented.
        Returns the supported sampling modes. They are returned (by reference) as a bit field. This bit field
        can be parsed using the IsBitSet Macro. Individual bits are defined using the FILTER constants in dwf.h.
        When the acquisition frequency (FDwfAnalogInFrequencySet) is less than the ADC frequency (maximum
        acquisition frequency).

        Calls the WaveForms API Function 'FDwfAnalogInChannelFilterInfo(HDWF hdwf, int *pfsfilter)'

        :param filter_number:
            - filterDecimate: 0
              Store every Nth ADC conversion, where N = ADC frequency /acquisition frequency.
            - filterAverage: 1
              Store the average of N ADC conversions.
            - filterMinMax: 2
              Store interleaved, the minimum and maximum values, of 2xN conversions.
            - filterAverageFit: 3
              The stored samples match the specified range instead of the device input range options.
              This can improve the vertical resolution of the samples.
        """
        WFAPI._check_device_connection(dwf, hdwf)
        raise NotImplementedError()

    @staticmethod
    def analog_in_channel_filter_set(dwf: CDLL, hdwf: c_int, channel: int, filter_number: int):
        """
        Not implemented.
        Sets the acquisition filter for each AnalogIn channel. With channel index -1, each enabled AnalogIn
        channel filter will be configured to use the same, new option.

        Calls the WaveForms API Function 'FDwfAnalogInChannelFilterSet(HDWF hdwf, int idxChannel, FILTER filter)'

        :param channel: Channel index
        :param filter_number: Acquisition sample filter to set.
            - filterDecimate: 0
              Store every Nth ADC conversion, where N = ADC frequency /acquisition frequency.
            - filterAverage: 1
              Store the average of N ADC conversions.
            - filterMinMax: 2
              Store interleaved, the minimum and maximum values, of 2xN conversions.
            - filterAverageFit: 3
              The stored samples match the specified range instead of the device input range options.
              This can improve the vertical resolution of the samples.
        """
        WFAPI._check_device_connection(dwf, hdwf)
        raise NotImplementedError()

    @staticmethod
    def analog_in_channel_filter_get(dwf: CDLL, hdwf: c_int, channel: int) -> int:
        """
        Not implemented.
        Returns the configured acquisition filter.

        Calls the WaveForms API Function 'FDwfAnalogInChannelFilterGet(HDWF hdwf, int idxChannel, FILTER *pfilter)'

        :param channel: Channel index
        :return: filter type (int)
            - filterDecimate: 0
              Store every Nth ADC conversion, where N = ADC frequency /acquisition frequency.
            - filterAverage: 1
              Store the average of N ADC conversions.
            - filterMinMax: 2
              Store interleaved, the minimum and maximum values, of 2xN conversions.
            - filterAverageFit: 3
              The stored samples match the specified range instead of the device input range options.
              This can improve the vertical resolution of the samples.
        """

    @staticmethod
    def analog_in_channel_range_info(dwf: CDLL, hdwf: c_int) -> tuple:
        """
        Returns the minimum and maximum range, peak to peak values, and the number of adjustable steps.
        The oscilloscope channel settings are identical across all channels.
        Calls WaveForms API Function
        'FDwfAnalogInChannelRangeInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps)'
        :return: The minimum and maximum range, peak to peak values, and the number of adjustable steps as a tuple
        (min, max, steps).
        """
        WFAPI._check_device_connection(dwf, hdwf)
        dbl0 = c_double()
        dbl1 = c_double()
        dbl2 = c_double()
        dwf.FDwfAnalogInChannelRangeInfo(hdwf, byref(dbl0), byref(dbl1), byref(dbl2))
        _range = (int(dbl0.value), int(dbl1.value), int(dbl2.value))
        return _range

    @staticmethod
    def analog_in_channel_range_steps(dwf: CDLL, hdwf: c_int):
        """
        Not implemented.
        Reads the range of steps supported by the device. For instance: 1, 2, 5, 10, etc.

        Calls WaveForms API Function
        'FDwfAnalogInChannelRangeSteps(HDWF hdwf, double rgVoltsStep[32], int *pnSteps)'
        """
        WFAPI._check_device_connection(dwf, hdwf)
        raise NotImplementedError()

    @staticmethod
    def analog_in_channel_range_set(dwf: CDLL, hdwf: c_int, channel: int, range: float):
        """
        Not implemented.
        Configures the range for each channel. With channel index -1, each enabled Analog In channel range
        will be configured to the same, new value.

        Calls WaveForms API Function
        'FDwfAnalogInChannelRangeSet(HDWF hdwf, int idxChannel, double voltsRange)'
        :param channel: Channel index
        :param range: The range to set.
        """
        WFAPI._check_device_connection(dwf, hdwf)
        raise NotImplementedError()

    @staticmethod
    def analog_in_channel_range_get(dwf: CDLL, hdwf: c_int, channel: int) -> float:
        """
        Not implemented.
        Returns the real range value for the given channel.

        Calls WaveForms API Function
        'FDwfAnalogInChannelRangeGet(HDWF hdwf, int idxChannel, double *pvoltsRange)'

        :param channel: Channel index
        :return: The real range value for the given channel.
        """

    @staticmethod
    def analog_in_channel_offset_info(dwf: CDLL, hdwf: c_int) -> tuple:
        """
        Returns the minimum and maximum offset levels supported, and the number of adjustable steps. The oscilloscope
        channel settings are identical across all channels.
        Calls WaveForms API Function
        'FDwfAnalogInChannelOffsetInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps)'
        :return: The minimum and maximum offset levels supported, and the number of adjustable steps as
        a tuple (min, max, steps).
        """
        WFAPI._check_device_connection(dwf, hdwf)
        dbl0 = c_double()
        dbl1 = c_double()
        dbl2 = c_double()
        dwf.FDwfAnalogInChannelOffsetInfo(hdwf, byref(dbl0), byref(dbl1), byref(dbl2))
        _offset = (int(dbl0.value), int(dbl1.value), int(dbl2.value))
        return _offset

    @staticmethod
    def analog_in_buffer_size(dwf: CDLL, hdwf: c_int) -> tuple:
        """
        Returns the minimum and maximum allowable buffer sizes for the instrument. The oscilloscope
        channel settings are identical across all channels.
        Calls WaveForms API Function 'FDwfAnalogInBufferSizeInfo(HDWF hdwf, int *pnSizeMin, int *pnSizeMax)'
        :return: The minimum and maximum allowable buffer sizes for the instrument as a tuple (min, max).
        """
        WFAPI._check_device_connection(dwf, hdwf)
        int0 = c_int()
        int1 = c_int()
        dwf.FDwfAnalogInBufferSizeInfo(hdwf, byref(int0), byref(int1))
        _buffer_size = (int(int0.value), int(int0.value))
        return _buffer_size

    @staticmethod
    def analog_in_bits(dwf: CDLL, hdwf: c_int) -> int:
        """
        Retrieves the number bits used by the AnalogIn ADC. The oscilloscope channel settings are identical
        across all channels.
        Calls WaveForms API Function 'FDwfAnalogInBitsInfo(HDWF hdwf, int *pnBits)'
        :return: The number bits used by the AnalogIn ADC.
        """
        int0 = c_int()
        WFAPI._check_device_connection(dwf, hdwf)
        dwf.FDwfAnalogInBitsInfo(hdwf, byref(int0))
        _adc_bits = int(int0.value)
        return _adc_bits


class WFAPIDeviceEnumeration(WFAPI):

    def __init__(self):
        super().__init__()

    @staticmethod
    def device_name(dwf: CDLL, device_id: int) -> str:
        """
        Retrieves the device name of the enumerated device.
        Calls WaveForms API Function 'FDwfEnumDeviceName(int idxDevice, char szDeviceName[32])'
        :return: The device name of the enumerated device
        """
        devicename = create_string_buffer(64)
        dwf.FDwfEnumDeviceName(c_int(device_id), devicename)
        return str(devicename.value.decode("utf-8"))

    @staticmethod
    def serial_number(dwf: CDLL, device_id: int) -> str:
        """
        Retrieves the serial number of the enumerated device.
        :return:
        """
        serialnum = create_string_buffer(16)
        dwf.FDwfEnumSN(c_int(device_id), serialnum)
        return str(serialnum.value.decode("utf-8"))

    @staticmethod
    def analog_in_channel_count(dwf: CDLL, device_id: int) -> int:
        """
        Returns the number of AnalogIn channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 1.
        :return: The number of analog in channels.
        """
        cInfo = c_int()
        # c_int(1): DECIAnalogInChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(1), byref(cInfo))
        return int(cInfo.value)

    @staticmethod
    def analog_out_channel_count(dwf: CDLL, device_id: int) -> int:
        """
        Returns the number of AnalogOut channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 2.
        :return: The number of analog out channels.
        """
        cInfo = c_int()
        # c_int(2): DECIAnalogOutChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(2), byref(cInfo))
        return int(cInfo.value)

    @staticmethod
    def analog_io_channel_count(dwf: CDLL, device_id: int) -> int:
        """
        Returns the number of AnalogIO channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 3.
        :return: The number of analog io channels.
        """
        cInfo = c_int()
        # c_int(3): DECIAnalogIOChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(3), byref(cInfo))
        return int(cInfo.value)

    @staticmethod
    def digital_in_channel_count(dwf: CDLL, device_id: int) -> int:
        """
        Returns the number of DigitalIn channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 4.
        :return: The number of digital in channels.
        """
        cInfo = c_int()
        # c_int(4): DECIDigitalInChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(4), byref(cInfo))

        return int(cInfo.value)

    @staticmethod
    def digital_out_channel_count(dwf: CDLL, device_id: int) -> int:
        """
        Returns the number of DigitalOut channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 5.
        :return: The number of digital out channels.
        """
        cInfo = c_int()
        # c_int(5): DECIDigitalOutChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(5), byref(cInfo))

        return int(cInfo.value)

    @staticmethod
    def digital_io_channel_count(dwf: CDLL, device_id: int) -> int:
        """
        Returns the number of DigitalIO channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 6.
        :return: The number of digital io channels.
        """
        cInfo = c_int()
        # c_int(6): DECIDigitalIOChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(6), byref(cInfo))
        return int(cInfo.value)

    @staticmethod
    def analog_in_buffer_size(dwf: CDLL, device_id: int) -> int:
        """
        Returns the buffer size of the AnalogIn channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 7.
        :return: The buffer size of the analog in channels.
        """
        cInfo = c_int()
        # c_int(6): DECIDigitalIOChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(7), byref(cInfo))
        return int(cInfo.value)

    @staticmethod
    def analog_out_buffer_size(dwf: CDLL, device_id: int) -> int:
        """
        Returns the buffer size of the AnalogOut channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 8.
        :return: The buffer size of the analog out channels.
        """
        cInfo = c_int()
        # c_int(6): DECIDigitalIOChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(8), byref(cInfo))
        return int(cInfo.value)

    @staticmethod
    def digital_in_buffer_size(dwf: CDLL, device_id: int) -> int:
        """
        Returns the buffer size of the DigitalIn channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 9.
        :return: The buffer size of the digital in channels.
        """
        cInfo = c_int()
        # c_int(6): DECIDigitalIOChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(9), byref(cInfo))
        return int(cInfo.value)

    @staticmethod
    def digital_out_buffer_size(dwf: CDLL, device_id: int) -> int:
        """
        Returns the buffer size of the DigitalOut channels of the device without opening it.
        Note: These are intended for preliminary information before opening a device. Further information are available
        with various the FDwf#Info functions.

        Calls WaveForms API Function 'FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pValue)'
        with parameter info = 10.
        :return: The buffer size of the digital out channels.
        """
        cInfo = c_int()
        # c_int(6): DECIDigitalIOChannelCount
        dwf.FDwfEnumConfigInfo(c_int(device_id), c_int(10), byref(cInfo))
        return int(cInfo.value)


class WFAPIDeviceControl(WFAPI):

    def __init__(self):
        super().__init__()

    @staticmethod
    def device_open(dwf: CDLL, device_id: int) -> c_int:
        """
        Opens a device identified by the enumeration index and retrieves a handle.
        To automatically enumerate all connected devices and open the first discovered device, use index -1.

        Calls WaveForms API Function 'FDwfDeviceOpen(int idxDevice, HDWF *phdwf)'

        :param dwf: Shared library handle.
        :param device_id: The device id of the device to open.
        :return: The handle (hdwf) of the opened device.
        """
        hdwf = c_int()
        dwf.FDwfDeviceOpen(c_int(device_id), byref(hdwf))
        return hdwf


class WaveFormsAPI:

    def __init__(self, parent_logger: logging.Logger):
        self._logger = parent_logger
        self.channels = WFAPIChannels()
        self.device_enumeration = WFAPIDeviceEnumeration()
        self.device_control = WFAPIDeviceControl()

        self._dwf_init = False
        self._dwf = None

    def init_dwf(self) -> CDLL:
        if not self._dwf_init:
            if sys.platform.startswith("win"):
                self._dwf = cdll.dwf
            elif sys.platform.startswith("darwin"):
                self._dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
            else:
                self._dwf = cdll.LoadLibrary("libdwf.so")
            self._dwf_init = True
        return self._dwf


    def get_connected_devices(self, dwf, discover_simulators: bool = False):
        self._logger.info(f"Discovering connected devices...")
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
        self._logger.debug(f"Filtering {type} devices...")
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
