import logging
import sys
from pathlib import Path
from multiprocessing import freeze_support


from PySide6.QtWidgets import QApplication
from rich.logging import RichHandler

import ADScopeControl as CaptDevice

#logging.disable(logging.INFO)

if __name__ == "__main__":
    freeze_support()

    def setup_logging():
        for log_name, log_obj in logging.Logger.manager.loggerDict.items():
            if log_name != '<module name>':
                log_obj.disabled = True
        # Format the Rich logger
        FORMAT = "%(message)s"
        logging.basicConfig(
            level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                RichHandler(rich_tracebacks=True)
            ]
        )

    setup_logging()
    app = QApplication()

    # The config class, that stores the configuration for the scope
    # using the confPy6 package (https://github.com/agentsmith29/confPy6).
    
    
    conf = CaptDevice.Config()
    
    conf_file = Path('./ADScopeConfig.yaml')
    if conf_file.exists():
        logging.info(f"Loading {conf_file}")
        conf.load(conf_file, as_auto_save=True)
    conf.autosave(enable=True, path='./')

    # --- Create the model, controller, and view. ---

    # Pass the config to the model.
    model = CaptDevice.Model(conf)

    # Pass the model and None to the controller.
    # The second argument start_capture_flag (here set to None) is a multiprocessing.Value that
    # triggers the scope.
    # This can be used to create a shared value between processes (e.g. a trigger by another process)
    controller = CaptDevice.Controller(
        model,
        None  # start_capture_flag: multiprocessing.Value, triggers the scope
    )

    # Create the view
    window = CaptDevice.View(model, controller)

    # Show the window
    window.show()

    sys.exit(app.exec())