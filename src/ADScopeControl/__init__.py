# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""


import ctypes
from pathlib import Path

from WidgetCollection.Tools.PyProjectExtractor import extract_pyproject_info
pytoml = Path(__file__).parent.parent.parent
__version__ = extract_pyproject_info(pytoml,"version")
__author__ = extract_pyproject_info(pytoml,"author")
__description__ = extract_pyproject_info(pytoml,"description")
__license__ = extract_pyproject_info(pytoml,"license")
__url__ = extract_pyproject_info(pytoml,"url")

# For correctly display the icon in the taskbar
myappid = f'agentsmith29.ADScopeControl.{__version__}'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from .CaptDeviceConfig import CaptDeviceConfig as Config
from .controller.BaseADScopeController import BaseADScopeController as Controller
from .model.AD2ScopeModel import AD2ScopeModel as Model
from .view.AD2CaptDeviceView import ControlWindow as View
