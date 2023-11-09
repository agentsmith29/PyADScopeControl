import os

from controller.AD2CaptDeviceController import AD2CaptDeviceController
from model.AD2CaptDeviceModel import AD2CaptDeviceModel
from view.AD2CaptDeviceView import ControlWindow

if os.environ.get('ADC_SIM') == "TRUE":
    pass
else:
    pass
# Init the AD model, controller and view
ad2_model = AD2CaptDeviceModel(vaut_config.ad2_device_config)
ad2_controller = AD2CaptDeviceController(ad2_model)
ad2_window = ControlWindow(ad2_model, ad2_controller)


