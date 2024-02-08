
# How to use this class
```
    app = QApplication()
    setup_logging()
    
    vaut_config = VAutomatorConfig.load_config("./configs/init_config.yaml")

    ad2_model = AD2CaptDeviceModel(vaut_config.ad2_device_config)
    ad2_controller = AD2CaptDeviceController(ad2_model)
    ad2_window = ControlWindow(ad2_model, ad2_controller)
    #ad2_controller.connect_device()
    #ad2_controller.start_capture()

    ad2_window.show()
    sys.exit(app.exec())
```