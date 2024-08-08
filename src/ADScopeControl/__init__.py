# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
"""

import ctypes
import os
import pathlib
from pathlib import Path

from WidgetCollection.Tools.PyProjectExtractor import extract_pyproject_info

from . import Helpers

# Directly in the repo

# ======================================================================================================================
# The pyconfig.toml file is needed, to get the metadata. Depending on the installation method (pip or git) the file
# is found in different places.
# ======================================================================================================================
pytoml = Helpers.get_pyprojecttoml()


def try_and_set(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error reading '{args[1]}' from {pathlib.Path(args[0])}: {e}")
        return "unknown"


__rootdir__ = os.path.dirname(os.path.realpath(__file__))
__version__ = try_and_set(extract_pyproject_info, pytoml.parent, "version")
__author__ = try_and_set(extract_pyproject_info, pytoml.parent, "author")
__description__ = try_and_set(extract_pyproject_info, pytoml.parent, "description")
__license__ = try_and_set(extract_pyproject_info, pytoml.parent, "license")
__url__ = try_and_set(extract_pyproject_info, pytoml.parent, "url")
# For correctly display the icon in the taskbar

myappid = f'agentsmith29.ADScopeControl.{__version__}'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from .CaptDeviceConfig import CaptDeviceConfig as Config
from .controller.BaseADScopeController import BaseADScopeController as Controller
from .model.AD2ScopeModel import AD2ScopeModel as Model
from .view.AD2CaptDeviceView import ControlWindow as View
