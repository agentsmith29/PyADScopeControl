# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""
import sys
from .CaptDeviceConfig import CaptDeviceConfig as Config
from .controller.AD2CaptDeviceController import AD2CaptDeviceController as Controller
from .model.AD2CaptDeviceModel import AD2CaptDeviceModel as Model
from .view.AD2CaptDeviceView import ControlWindow as View