# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
import confighandler as cfg


class CaptDeviceConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()
        self.sample_rate = cfg.Field(500, friendly_name="Sample rate",
                                     description="Sample rate of the device")
        self.streaming_rate = cfg.Field(500, friendly_name="Streaming rate",
                                     description="Streaming rate in Hz (should be below 1kHz)")

        self.ain_channel = cfg.Field(0, friendly_name="Analog In Channel",
                                     description="Analog in channel. Defines which channel is used for capturing.")
        self.show_simulator = cfg.Field(True, friendly_name="Show Simulators",
                                        description="Show available simulators in the device list "
                                                    "provided by the DreamWaves API.")
        self.streaming_history = cfg.Field(2000, friendly_name="Streaming history (ms)",
                                        description="Defines the range of the stream in ms")



        # TODO: Old configs (not used and will probably removed in future)
        self.total_samples = cfg.Field(200000)
        self.sample_time = cfg.Field(45)
        self.ad2_raw_out_file = cfg.Field("{output_directory}/measurement/ad2_raw/ad2_out_{wafer_nr}_{date}.csv")

        self.register()

