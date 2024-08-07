# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
from ctypes import CDLL

from ADScopeControl.controller.DeviceInformation.AnalogOutChannel import AnalogOutChannels
from ADScopeControl.controller.DeviceInformation.dataclasses.AnalogInChannelInfo import AnalogInChannels


class HWConnectedDeviceInformation:
    """ Class for storing information about the connected device."""

    def __init__(self, dwf: CDLL, device_idx, type="USB"):
        self.dwf = dwf
        self._type: str = type

        self._device_id: int = device_idx
        self._device_name: str = ""
        self._serial_number: str = ""

        self.analog_in_channels = list[AnalogInChannels]
        self.analog_out_channels = list[AnalogOutChannels]

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

    def __repr__(self):
        return f"HW({self._device_name}, {self._serial_number}, {self._type})"