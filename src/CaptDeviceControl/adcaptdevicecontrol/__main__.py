"""
Main File for testing the module
(c) Christoph Schmidt, 2023
christoph.schmidt@tugraz.at
"""


import logging
import sys

#from generics.logger import setup_logging


from PySide6.QtWidgets import QApplication
from rich.logging import RichHandler
sys.path.append('../adcaptdevicecontrol')

import adcaptdevicecontrol
from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig

if __name__ == "__main__":
    app = QApplication()
    #setup_logging()

    logging.warning("AD2CaptDeviceController.py is not meant to be run as a script.")

    # This path is not included in this module. It is only included in flexsensorpy
    # See the git repo under ./flexsensorpy/configs/init_config.yaml
    vaut_config = VAutomatorConfig.load_config("../../configs/init_config.yaml")


    ad2_window.show()
    sys.exit(app.exec())