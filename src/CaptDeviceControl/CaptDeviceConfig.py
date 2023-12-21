# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
import logging

import confighandler as cfg


class CaptDeviceConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__(internal_log=True, internal_log_level=logging.DEBUG)
        self.sample_rate = cfg.Field(500, friendly_name="Sample rate",
                                     description="Sample rate of the device")
        self.streaming_rate = cfg.Field(500, friendly_name="Streaming rate",
                                     description="Streaming rate in Hz (should be below 1kHz)")


        self.ain_channel = cfg.Field(
            cfg.SelectableList([0, 1],
                               description=["Channel 0", "Channel 1"],
                               selected_index=0,
                               ),
            friendly_name="Analog In Channel",
            description="Analog in channel. Defines which channel is used for capturing.")

        self.show_simulator = cfg.Field(True, friendly_name="Show Simulators",
                                        description="Show available simulators in the device list "
                                                    "provided by the DreamWaves API.")
        self.streaming_history = cfg.Field(
            cfg.SelectableList([100, 200, 500 ,1000, 2000, 5000, 10000, 20000, 30000],
                               description=["100 ms", "200 ms", "500 ms", "1 s", "2 s", "5 s", "10 s", "20 s", "30 s"],
                               selected_index=3,
                               ),
            friendly_name="Streaming history",
            description="Defines the range of the stream in ms")



        # TODO: Old configs (not used and will probably removed in future)
        self.total_samples = cfg.Field(200000)
        self.sample_time = cfg.Field(45)
        self.ad2_raw_out_file = cfg.Field("{output_directory}/measurement/ad2_raw/ad2_out_{wafer_nr}_{date}.csv")

        self.register()

