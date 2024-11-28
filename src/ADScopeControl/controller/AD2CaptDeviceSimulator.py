import time
from datetime import datetime

import scipy
from PySide6.QtCore import Slot

from ADScopeControl.controller.BaseADScopeController import BaseADScopeController

class ADScopeSimulator(BaseADScopeController):


    def connect_device(self, device_id):
        self.logger.info("Connecting to simulator")
        self._init_device_parameters()
        self.model.dwf_version = "DWF SIM 1.0"
        self.logger.info(f"[{self.pref} Report] DWF Version: {self.model.dwf_version}")

        self.logger.info(f"[{self.pref} Task] Opening device Simulator...")
        self.model.device_name = "ADC Simulator"
        self.model.device_serial_number = "Simulator"
        #
        self.model.ain_device_state = 0
        self.model.connected = True
        self.update_device_information()
        self.logger.info(f"[{self.pref} Task] Device connected!")
        return True

    def discover_connected_devices(self):
        self.model.connected_devices = {
            'type':  "Simulator",
            'device_id': 0,
            'device_name': "Simulator AD2",
            'serial_number': "0000"
           }

    @Slot()
    def start_capturing_process(self, capture):

        if capture:
            self.logger.info(f"[{self.pref} Task] Setting up device for capturing.")

            # if self._setup_acquisition():
            #    self.logger.info(f"[{self.pref} Task] Started capturing thread")
            self.set_ad2_acq_status(True)
            return self.thread_manager.start(self._capture)
        else:
            self.set_ad2_acq_status(False)
        # return self._capture()

    def _capture(self):
        self.model.capturing_finished = False
        self.model.device_capturing_state = False
        # Read the mat file from ./support
        matf = scipy.io.loadmat("./support/simulator_support.mat")
        self.model.device_ready = True
        t0 = -1
        curr_sample = 0
        while True:
            if self.model.start_recording and not self.model.stop_recording:
                if t0 < 0:
                    self.logger.info(f"[{self.pref} Report] Start command received.")
                    self.model.capturing_finished = False
                    self.model.device_capturing_state = True
                    self.model.recorded_samples = self.model.recorded_samples.clear()
                    timestamp = datetime.now()
                    t0 = time.time()
                else:
                    curr_sample += 1
                    try:
                        # print(matf['amplitude'].flatten()[curr_sample])
                        if curr_sample % 200 == 0:
                            t2 = time.time()
                            # Append 10 samples at a time
                            self.model.recorded_samples.extend(
                                matf['amplitude'].flatten()[curr_sample-99:curr_sample]
                            )
                            t3 = time.time()
                            #print(f"{curr_sample}: Time took {t3-t2}")

                    except Exception as e:
                        print(e)

            elif not self.model.start_recording and self.model.stop_recording:
                t1 = time.time()
                self.model.measurement_time = t1 - t0
                # self.get_analog_in_status()
                self.model.capturing_finished = True
                self.model.device_capturing_state = False
                self.logger.info(f"Finished Thread. Acquisition took {self.model.measurement_time} s. "
                                 f"Process captured {len(self.model.recorded_samples)} samples.")
                # 1. Assign the current captured samples to a dict
                self.model.all_recorded_samples.append({'timestamp': timestamp,
                                                        'measurement_time': self.model.measurement_time,
                                                        'num_samples': len(
                                                            self.model.recorded_samples),
                                                        'acqRate': self.model.sample_rate,
                                                        'samples': self.model.recorded_samples})
                try:
                    time.sleep(1)
                    self.close_device()
                except Exception as e:
                    print(e)
                return

    def update_device_information(self):
        self.model.ain_channels = [0]
        self.model.ain_buffer_size = 1
        self.model.aout_channels = [0]
        self.model.selected_ain_channel = 1

    def close_device(self):
        # Resets and configures (by default, having auto configure enabled) all AnalogOut instrument
        # parameters to default values for the specified channel. To reset instrument parameters across all
        # channels, set idxChannel to -1.
        self.model.fLost = 0
        self.model.fCorrupted = 0
        self.model.start_recording = True
        self.model.stop_recording = False
        self.model.capturing_finished = False
        self.model.device_capturing_state = False
        self.model.connected = False
        self.model.ain_device_state = 0
        self.model.dwf_version = "Unknown"
        self.model.device_serial_number = "Unknown"
        self.model.device_name = "Unknown"
        self.model.selected_ain_channel = -1
        self.logger.info(f"[{self.pref} Task] Device closed.")
