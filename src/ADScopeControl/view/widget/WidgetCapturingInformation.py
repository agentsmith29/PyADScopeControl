from PySide6.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel

from WidgetCollection.widgets.LEDIndicatorWidget import LEDIndicatorWidget


class WidgetCapturingInformation(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.init_UI()

    def init_UI(self):
        grid_group_box = QGroupBox("Capturing Information")
        layout = QGridLayout()

        self.lbl_conn_state = QLabel("Connection state unknown")
        self.led_conn_state = LEDIndicatorWidget(color="gray")
        layout.addWidget(self.led_conn_state, 0, 0)
        layout.addWidget(self.lbl_conn_state, 0, 1)

        self.lbl_is_capt = QLabel("Not capturing")
        self.led_is_capt = LEDIndicatorWidget(color="red")
        layout.addWidget(self.led_is_capt, 1, 0)
        layout.addWidget(self.lbl_is_capt, 1, 1)

        self.lbl_device_state = QLabel("Device State Unknown")
        self.led_device_state = LEDIndicatorWidget(color="gray")
        layout.addWidget(self.led_device_state, 2, 0)
        layout.addWidget(self.lbl_device_state, 2, 1)



        grid_group_box.setLayout(layout)
        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)


class WidgetDeviceInformation(QWidget):
    def __init__(self):
        super().__init__()

        self._serial_number = ""
        self._dwf_version = ""
        self._device_name = ""
        self._sample = ""
        self._analog_in_channel = ""

        self.layout = QGridLayout()

        self.init_UI()

    @property
    def analog_in_channel(self):
        return self._analog_in_channel

    @analog_in_channel.setter
    def analog_in_channel(self, value):
        self._analog_in_channel = value
        self.lbl_analog_in_channel.setText(f"Analog In: {self._analog_in_channel}")

    @property
    def dwf_version(self):
        return self._dwf_version

    @dwf_version.setter
    def dwf_version(self, value):
        self._dwf_version = value
        self.lbl_dwf_version.setText(f"DWF Version: {self._dwf_version}")

    @property
    def device_name(self):
        return self._device_name

    @device_name.setter
    def device_name(self, value):
        self._device_name = value
        self.lbl_device_name.setText(f"Name: {self._device_name}")

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, value):
        self._sample = value
        self.lbl_if_handle.setText(f"Sample: {self._sample}")

    @property
    def serial_number(self):
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value):
        self._serial_number = value
        self.lbl_serial_number.setText(f"Serial Number: {self._serial_number}")

    def init_UI(self):
        grid_group_box = QGroupBox("Device Information")
        layout = QGridLayout()

        self.lbl_dwf_version = QLabel("DWF Version: Unknown")
        layout.addWidget(self.lbl_dwf_version, 0, 0)

        self.lbl_serial_number = QLabel("Serial Number: Unknown")
        layout.addWidget(self.lbl_serial_number, 1, 0)

        self.lbl_device_name = QLabel("Name: Unknown")
        layout.addWidget(self.lbl_device_name, 2, 0)

        self.lbl_if_handle = QLabel("Samples: Unknown")
        layout.addWidget(self.lbl_if_handle, 3, 0)

        self.lbl_analog_in_channel = QLabel("AnalogIn Channel: Unknown")
        layout.addWidget(self.lbl_analog_in_channel, 4, 0)

        grid_group_box.setLayout(layout)
        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)

class WidgetSupervisionInformation(QWidget):
    def __init__(self):
        super().__init__()

        self._supervised = False
        self._supervisor_name = "Unknown"

        self.layout = QGridLayout()

        self.init_UI()

    @property
    def supervised(self):
        return self._supervised

    @supervised.setter
    def supervised(self, value):
        self._supervised = value
        self.lbl_supervised.setText(f"Supervised: {self.supervised}")

    @property
    def supervisor_name(self):
        return self._supervisor_name

    @supervisor_name.setter
    def supervisor_name(self, value):
        self._supervisor_name = value
        self.lbl_supervisor.setText(f"Supervisor: {self.supervisor_name}")

    def init_UI(self):
        grid_group_box = QGroupBox("Device Information")
        layout = QGridLayout()

        self.lbl_supervised = QLabel("Supervised: Unknown")
        layout.addWidget(self.lbl_supervised, 0, 0)

        self.lbl_supervisor = QLabel("Supervisor: Unknown")
        layout.addWidget(self.lbl_supervisor, 1, 0)

        grid_group_box.setLayout(layout)
        self.layout.addWidget(grid_group_box)
        self.setLayout(self.layout)






