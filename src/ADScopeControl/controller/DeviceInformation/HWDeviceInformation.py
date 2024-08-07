# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
from ctypes import CDLL

from ADScopeControl.controller.DeviceInformation.WaveFormsAPI import WFAPIDeviceEnumeration, WFAPIDeviceControl, WFAPIChannels
from ADScopeControl.controller.DeviceInformation.dataclasses.AnalogInChannelInfo import AnalogInChannelInfo, AnalogInChannelRetriever


class HWDeviceInformation:
    """ Class for storing information about the connected device."""

    def __init__(self, device_idx, type="USB"):
        self._type: str = type

        self._device_id: int = device_idx
        self._device_name: str = ""
        self._serial_number: str = ""

        self._analog_in_channels: list[AnalogInChannelInfo] = []
        self._analog_out_channels: list[AnalogInChannelInfo] = []

        self._analog_in_channel_count: int = 0
        self._analog_out_channel_count: int = 0
        self._analog_io_channel_count: int = 0

        self._digital_in_channel_count: int = 0
        self._digital_out_channel_count: int = 0
        self._digital_io_channel_count: int = 0

        self._analog_in_buffer_size: int = 0
        self._analog_out_buffer_size: int = 0

        self._digital_in_buffer_size: int = 0
        self._digital_out_buffer_size: int = 0
        # self._reload()

    @property
    def type(self) -> str:
        """
        Returns the type of the device (USB or Simulator)
        :return: Type of the device
        """
        return self._type

    @property
    def device_id(self) -> int:
        """
        The device id of the enumerated device.
        :return: The device id of the enumerated device.
        """
        return self._device_id

    @property
    def device_name(self) -> str:
        """
        The device name of the enumerated device.
        :return: The device name of the enumerated device.
        """
        return self._device_name

    @property
    def serial_number(self) -> str:
        """
        The serial number of the enumerated device.
        :return: The serial number of the enumerated device.
        """
        return self._serial_number

    @property
    def analog_in_channels(self) -> list[AnalogInChannelInfo]:
        """
        The analog in channels of the device without opening it.
        :return: The analog in channels.
        """
        return self._analog_in_channels

    @property
    def analog_out_channels(self) -> list[AnalogInChannelInfo]:
        """
        The analog out channels of the device without opening it.
        :return: The analog out channels.
        """
        return self._analog_out_channels

    @property
    def analog_in_channel_count(self) -> int:
        """
        The number of AnalogIn channels of the device without opening it.
        :return: The number of analog in channels.
        """
        return self._analog_in_channel_count

    @property
    def analog_out_channel_count(self) -> int:
        """
        The number of AnalogOut channels of the device without opening it.
        :return: The number of analog out channels.
        """
        return self._analog_out_channel_count

    @property
    def analog_io_channel_count(self) -> int:
        """
        The number of AnalogIO channels of the device without opening it.
        :return: The number of analog io channels.
        """
        return self._analog_io_channel_count

    @property
    def digital_in_channel_count(self) -> int:
        """
        The number of DigitalIn channels of the device without opening it.
        :return: The number of digital in channels.
        """
        return self._digital_in_channel_count

    @property
    def digital_out_channel_count(self) -> int:
        """
        The number of DigitalOut channels of the device without opening it.
        :return: The number of digital out channels.
        """
        return self._digital_out_channel_count

    @property
    def digital_io_channel_count(self) -> int:
        """
        The number of DigitalIO channels of the device without opening it.
        :return: The number of digital io channels.
        """
        return self._digital_io_channel_count

    @property
    def analog_in_buffer_size(self) -> int:
        """
        The buffer size of the AnalogIn channels of the device without opening it.
        :return: The buffer size of the analog in channels.
        """
        return self._analog_in_buffer_size

    @property
    def analog_out_buffer_size(self) -> int:
        """
        The buffer size of the AnalogOut channels of the device without opening it.
        :return: The buffer size of the analog out channels.
        """
        return self._analog_out_buffer_size

    @property
    def digital_in_buffer_size(self) -> int:
        """
        The buffer size of the DigitalIn channels of the device without opening it.
        :return: The buffer size of the digital in channels.
        """
        return self._digital_in_buffer_size

    @property
    def digital_out_buffer_size(self) -> int:
        """
        The buffer size of the DigitalOut channels of the device without opening it.
        :return: The buffer size of the digital out channels.
        """
        return self._digital_out_buffer_size

    def __repr__(self):
        return f"HW({self._device_name}, {self._serial_number}, {self._type})"


class HWDeviceInformationRetriever(HWDeviceInformation):
    def __init__(self, dwf: CDLL, device_idx, con_type="USB"):
        super().__init__(device_idx, con_type)
        self._device_name = WFAPIDeviceEnumeration.device_name(dwf, self.device_id)
        self._serial_number = WFAPIDeviceEnumeration.serial_number(dwf, self.device_id)

        # Top get all settings, we need to open the device
        try:
            self.hwdf = WFAPIDeviceControl.device_open(dwf, self.device_id)
        except Exception as ex:
            print(f"Error opening device: {ex}")
            self.hwdf = None

        if self.hwdf is not None:
            # Get the number of ain channels
            channel_count = WFAPIChannels().analog_in_channels_count(dwf,  self.hwdf)
            #print(channel_count)
            # Create a list of channels
            for channel in range(channel_count):
                o = AnalogInChannelRetriever(dwf, self.hwdf, channel).simple()
                self._analog_in_channels.append(o)
                print(type(o))

            self._analog_in_channel_count = len(self._analog_in_channels)


    def simple(self):
        return super()
