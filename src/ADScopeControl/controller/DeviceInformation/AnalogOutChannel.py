# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
from ctypes import CDLL, c_int, byref

from ADScopeControl.controller.DeviceInformation.HWDeviceBase import HWDeviceBase


class AnalogOutChannel(HWDeviceBase):
    def __init__(self, dwf: CDLL, hwdf: c_int, device_idx, channel):
        super().__init__(dwf, hwdf)

        self._channel: int = channel
        self._node: int = 0
        self._buffer_size: int = 0
        self._amplitude: tuple = (0, 0)
        self._offset: tuple = (0, 0)
        self._frequency: tuple = (0, 0)

    def reinit(self, fields: dict):
        for k, v in fields.items():
            setattr(self, k, v)

    @property
    def channel(self) -> int:
        """
            Returns the channel number of the AnalogOut channel.
            :return: The channel number of the AnalogOut channel.
        """
        return self._channel

    @property
    def node(self) -> int:
        """
            Returns the node number of the AnalogOut channel.
            :return: The node number of the AnalogOut channel.
        """
        return self._node

    @property
    def buffer_size(self) -> int:
        """
            Reads the number of AnalogIn channels of the device. The oscilloscope channel settings are
            identical across all channels.
            Calls WaveForms API Function 'FDwfAnalogInChannelCount(HDWF hdwf, int *pcChannel)'
            :return: The number of analog in channels.
        """
        self._check_device_connection()
        int0 = c_int()
        self.dwf.FDwfAnalogInChannelCount(self.hdwf, byref(int0))
        self._analog_in_channels = int(int0.value)
        return self._analog_in_channels


class AnalogOutChannelSetter():
    pass