# ADCaptDeviceControl



## Getting started

This is the module which allows to control an Analog Discovery device from Digilent. It is based on the [Analog Discovery SDK](https://reference.digilentinc.com/reference/software/waveforms/waveforms-3/reference-manual) and the [Waveforms SDK](https://reference.digilentinc.com/reference/software/waveforms/waveforms-3/reference-manual).
The module is made to stream and capture the data. 

### Prerequisites
The Analog Discovery only works with the correct SDK installed. 
The SDK can be found [here](https://reference.digilentinc.com/reference/software/waveforms/waveforms-3/start).
The SDK is only available for Windows, Mac and Linux. The module is only tested on Windows.

## Using the module
### Logging setup
This step is not mandatory, however helps you to see what is happening in the background.
Jus implement the following code in your main file and run the function
```python
import logging
from rich.logging import RichHandler

def setup_logging(window: ConsoleWindow = None):
    for log_name, log_obj in logging.Logger.manager.loggerDict.items():
        if log_name != '<module name>':
            log_obj.disabled = True
    # Format the Rich logger
    FORMAT = "%(message)s"
    if window is not None:
        logging.basicConfig(
            level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                RichHandler(rich_tracebacks=True), window.handler
            ]
        )
    else:
        logging.basicConfig(
            level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                RichHandler(rich_tracebacks=True)
            ]
        )
# Setup the logging formatter.
setup_logging()

```
THis makes sure to have proper logging formatting.
### Connecting the model, controller and view
The module can be run with 
````python
# This path is not included in this module. It is only included in flexsensorpy
# See the git repo under ./flexsensorpy/configs/init_config.yaml
vaut_config = VAutomatorConfig.load_config("../../configs/init_config.yaml")

# Init the AD model, controller and view
ad2_model = AD2CaptDeviceModel(vaut_config.ad2_device_config)
ad2_controller = AD2CaptDeviceController(ad2_model)
ad2_window = ControlWindow(ad2_model, ad2_controller)

ad2_window.show()
sys.exit(app.exec())
````