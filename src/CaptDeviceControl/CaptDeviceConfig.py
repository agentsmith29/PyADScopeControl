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
        self.sample_rate = cfg.Field(50000)
        self.total_samples = cfg.Field(200000)
        self.sample_time = cfg.Field(45)
        self.ad2_raw_out_file = cfg.Field("{output_directory}/measurement/ad2_raw/ad2_out_{wafer_nr}_{date}.csv")
        self.register()

