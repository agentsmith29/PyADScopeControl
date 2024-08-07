# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
from ctypes import CDLL, c_int
from dataclasses import dataclass

from ADScopeControl.controller.DeviceInformation.WaveFormsAPI import WFAPIChannels


@dataclass
class AnalogInChannelInfo:
    """ Class for storing the information about the channels"""

    def __init__(self):
        self._channel = 0
        self._buffer_size: tuple = (0, 0)
        self._adc_bits: int = 0
        self._range: tuple = (0, 0, 0)
        self._offset: tuple = (0, 0, 0)

    @property
    def buffer_size(self) -> tuple:
        """ Returns the minimum and maximum allowable buffer sizes for the instrument"""
        return self._buffer_size

    @property
    def adc_bits(self) -> int:
        """ Returns the number bits used by the AnalogIn ADC"""
        return self._adc_bits

    @property
    def range(self) -> tuple:
        """ Returns the minimum and maximum range, peak to peak values, and the number of adjustable steps"""
        return self._range

    @property
    def offset(self) -> tuple:
        """ Returns the minimum and maximum offset levels supported, and the number of adjustable steps"""
        return self._offset


class AnalogInChannelRetriever(AnalogInChannelInfo):

    def __init__(self, dwf: CDLL, hwdf: c_int, channel: int):
        super().__init__()
        self._channel = channel
        self._buffer_size: tuple = WFAPIChannels().analog_in_buffer_size(dwf, hwdf)
        self._adc_bits: int = WFAPIChannels().analog_in_bits(dwf, hwdf)
        self._range: tuple = WFAPIChannels().analog_in_channel_range_info(dwf, hwdf)
        self._offset: tuple = WFAPIChannels().analog_in_channel_offset_info(dwf, hwdf)

    def simple(self):
        # TODO: Does nto work
        return super(AnalogInChannelInfo, self)