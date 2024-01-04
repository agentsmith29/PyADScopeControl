# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
from ctypes import CDLL, c_int, create_string_buffer


class HWDeviceBase:
    """Base class for retrieving information from the hardware."""

    def __int__(self, dwf: CDLL, hwdf: c_int):
        self.dwf: CDLL = dwf
        self.hdwf: hwdf = hwdf

    def _check_device_connection(self):
        if self.hdwf.value == 0:
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            raise Exception(str(szerr.value))


