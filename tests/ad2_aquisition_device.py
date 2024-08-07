
from PySide6.QtCore import Signal, QObject
from datetime import time

# Needed for Digilent Analog Discovery 2 data acquisition	
from ctypes import *
import time
import logging

from rich.logging import RichHandler

from CaptDeviceControl.constants.dwfconstants import hdwfNone, acqmodeRecord


class AD2CaptDeviceSignals(QObject):
    dwf_version = Signal(str)
    connected = Signal(bool)

    ad2_settings = Signal(dict)

    error = Signal(str)

    ad2_is_capturing = Signal(bool)

    ad2_set_acquisition = Signal(bool)

class AD2CaptDevice():
    def __init__(self):
        self.pref = "AD2CaptDev"
        self.logger  = logging.getLogger(f"AD2 Device")
        self.signals = AD2CaptDeviceSignals()
        self.dwf = cdll.dwf

    def init(self):

        self.hdwf = c_int()
        self.sts = c_byte()
        self.hzAcq = c_double(10000)
        self.nSamples = int(20000)
        self.rgdSamples = (c_double*int(self.nSamples))()
        self.cAvailable = c_int()
        self.cLost = c_int()
        self.cCorrupted = c_int()
        self.fLost = 0
        self.fCorrupted = 0
        self.curr_settings = {
            "hdwf": self.hdwf ,
            "sts": self.sts,
            "hzAcq": self.hzAcq,
            "nSamples": self.nSamples,
            "rgdSamples": self.rgdSamples,
            "cAvailable": self.cAvailable,
            "cLost": self.cLost,
            "cCorrupted": self.cCorrupted,
            "fLost":self.fLost,
            "fCorrupted": self.fCorrupted,
        }


    def connect(self):
        self._setup_device()
        # open device
        self.logger.info(f"[{self.pref} Task] Opening device...")
        self.dwf.FDwfDeviceOpen(c_int(-1), byref(self.hdwf))
        if self.hdwf.value == hdwfNone.value:
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            # print(str(szerr.value))
            self.signals.connected.emit(False)
            raise Exception("Failed to open device: %s" % str(szerr.value))
        self.logger.info(f"[{self.pref} Task] Device connected!")

        self.signals.connected.emit(True)
        self.signals.dwf_version.emit(self.version)
        self.signals.ad2_settings.emit(self.curr_settings)
        return True

    def _setup_device(self):


        version = create_string_buffer(16)
        self.dwf.FDwfGetVersion(version)
        self.version = str(version.value)
        self.logger.info(f"[{self.pref} Report] DWF Version: {self.version}")


    def setup_acquisition(self):
        # set up acquisition
        self.logger.debug(f"[{self.pref} Task] Setup for acquisition. Wait 2 seconds for the offset to stabilize.")
        self.dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(0), c_bool(True))
        self.dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(0), c_double(5))
        self.dwf.FDwfAnalogInAcquisitionModeSet(self.hdwf, acqmodeRecord)
        self.dwf.FDwfAnalogInFrequencySet(self.hdwf, self.hzAcq)
        self.dwf.FDwfAnalogInRecordLengthSet(self.hdwf,
                                             c_double(self.nSamples / self.hzAcq.value))  # -1 infinite record length

        # wait at least 2 seconds for the offset to stabilize
        time.sleep(2)
        self.logger.info(f"[{self.pref} Task] Setup for acquisition done.")

        return True

    def on_ad2_set_acquisition_changed(self, record):
        if record:
            print("Started acquisiton!")
        else:
            print("Stopped acquisiton!")

    def analog_in_record(self, file_out):


if __name__ == "__main__":

    def setup_logging():
        for log_name, log_obj in logging.Logger.manager.loggerDict.items():
            if log_name != '<module name>':
                log_obj.disabled = True
        # Format the Rich logger
        FORMAT = "%(message)s"
        logging.basicConfig(
            level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                RichHandler(rich_tracebacks=True)
            ]
        )


    setup_logging()

    ad2 = AD2CaptDevice()
    #ad2.init()
    #ad2.connect()
    ad2.analog_in_record('test.txt')