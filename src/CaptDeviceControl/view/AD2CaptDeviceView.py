import logging

import numpy as np

from PySide6.QtCore import QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QStatusBar
from pyqtgraph.dockarea import DockArea, Dock

import pyqtgraph as pg

from controller.AD2CaptDeviceController import AD2CaptDeviceController
from model.AD2CaptDeviceModel import AD2CaptDeviceModel
from model.AD2Constants import AD2Constants
from view.Ui_AD2ControlWindow import Ui_AD2ControlWindow
from view.widget.WidgetCapturingInformation import WidgetCapturingInformation, WidgetDeviceInformation

from constants.dwfconstants import DwfStateReady, DwfStateConfig, DwfStatePrefill, DwfStateArmed, DwfStateWait, \
    DwfStateTriggered, DwfStateRunning, DwfStateDone
from fswidgets import PlayPushButton


class ControlWindow(QMainWindow):

    def __init__(self, model: AD2CaptDeviceModel, controller: AD2CaptDeviceController):
        super().__init__()
        self.logger = logging.getLogger("AD2ControlWindow")

        self.controller = controller
        self.model = model

        self._ui = Ui_AD2ControlWindow()
        self._ui.setupUi(self)
        #

        self.capt_info = WidgetCapturingInformation()
        self.dev_info = WidgetDeviceInformation()
        self._ui.grd_information.addWidget(self.capt_info, 0, 0, 1, 1)
        self._ui.grd_information.addWidget(self.dev_info, 0, 1, 1, 1)

        # The Information Widgets
        self._ui.grd_plot.addWidget(self._init_UI_live_plot(), 1, 0, 1, 1)
        # self._ui.grd_information.addWidget(self.init_UI_ad2_settings(), 3, 0, 1, 2)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Timer for periodically updating the plot
        self.capture_update_timer = QTimer()
        self.capture_update_timer.setInterval(50)
        self.capture_update_timer.timeout.connect(self._on_capture_update_plot)

        self.stream_update_timer = QTimer()
        self.stream_update_timer.setInterval(50)
        self.stream_update_timer.timeout.connect(self._on_stream_update_timer_timeout)

        self.stream_samples_frequency = 1000
        self.stream_n = 1

        # Connect the signals and controls
        self._connect_controls()
        self._connect_signals()
        self._init_other_ui_elements()
        self._ui.cb_duration_streaming_history.setCurrentIndex(5)

        self.controller.discover_connected_devices()

        self.model.sample_rate = self.model.ad2captdev_config.sample_rate.value

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def _connect_controls(self):
        self._ui.btn_connect.clicked.connect(self.on_btn_connect_to_device_clicked)
        self._ui.btn_start_capture.clicked.connect(self.on_btn_start_capture_clicked)
        self._ui.btn_stop.clicked.connect(self.on_btn_stop_clicked)

        # self._ui.sb_acquisition_rate.valueChanged.connect(self.on_btn_stop_clicked)
        self.model.ad2captdev_config.sample_rate.view.add_new_view(self._ui.sb_acquisition_rate)
        #()

        self._ui.cb_duration_streaming_history.currentIndexChanged.connect(
            self._on_cb_duration_streaming_history_currentIndexChanged)

    def _connect_signals(self):
        # WaveForms Runtime (DWF) Information
        self.model.signals.dwf_version_changed.connect(self._on_dwf_version_changed)

        # Connected Device Information
        self.model.signals.num_of_connected_devices_changed.connect(self._on_num_of_connected_devices_changed)
        self.model.signals.connected_devices_changed.connect(self._on_connected_devices_changed)

        # Device information
        self.model.signals.connected_changed.connect(self._on_connected_changed)
        self.model.signals.device_name_changed.connect(self._on_device_name_changed)
        self.model.signals.serial_number_changed.connect(self._on_device_serial_number_changed)
        self.model.signals.device_index_changed.connect(self._on_device_index_changed)

        # Acquisition Settings
        self.model.signals.sample_rate_changed.connect(self._on_sample_rate_changed)
        self.model.signals.selected_ain_channel_changed.connect(self._on_selected_ain_channel_changed)

        # Analog In Information
        self.model.signals.ain_channels_changed.connect(self._on_ain_channels_changed)
        self.model.signals.ain_buffer_size_changed.connect(self._on_ain_buffer_size_changed)
        self.model.signals.ain_bits_changed.connect(self._on_ain_bits_changed)
        self.model.signals.ain_device_state_changed.connect(self._on_ain_device_state_changed)


        # Analog Out Information
        self.model.signals.aout_channels_changed.connect(self._on_aout_channels_changed)

        # Acquired Signal Information
        self.model.signals.recorded_samples_changed.connect(self._on_recorded_samples_changed)
        self.model.signals.recording_time_changed.connect(self._on_recording_time_changed)
        self.model.signals.samples_captured_changed.connect(self._on_samples_captured_changed)
        self.model.signals.samples_lost_changed.connect(self._on_samples_lost_changed)
        self.model.signals.samples_corrupted_changed.connect(self._on_samples_corrupted_changed)

        # Recording Flags (starting, stopping and pausing)
        self.model.signals.device_capturing_state_changed.connect(self._on_device_capturing_state_changed)
        self.model.signals.start_recording_changed.connect(self._on_start_recording_changed)
        self.model.signals.stop_recording_changed.connect(self._on_stop_recording_changed)
        self.model.signals.reset_recording_changed.connect(self._on_reset_recording_changed)

        # Multiprocessing Information
        self.model.signals.pid_changed.connect(self._on_pid_changed)


        # Plotting Timer (periodically updating the plot)
        # self.capture_update_timer.timeout.connect(self._on_capture_update_plot)

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def _init_UI_live_plot(self):
        area = DockArea()

        d1 = Dock("Analog Discovery 2")
        area.addDock(d1, 'top')

        d2 = Dock("Captured Data")
        area.addDock(d2, 'bottom')

        self.scope_original = pg.PlotWidget(title="AD2 Acquisition")
        self.scope_original.plotItem.showGrid(x=True, y=True, alpha=1)
        d1.addWidget(self.scope_original)
        self.scope_original.setYRange(-1.5, 1.5, padding=0)

        self.scope_captured = pg.PlotWidget(title="Captured Data")
        self.scope_captured.plotItem.showGrid(x=True, y=True, alpha=1)
        d2.addWidget(self.scope_captured)

        return area

    def _init_other_ui_elements(self):
        self._ui.cb_duration_streaming_history.addItem("100ms", 0.1)
        self._ui.cb_duration_streaming_history.addItem("200ms", 0.2)
        self._ui.cb_duration_streaming_history.addItem("500ms", 0.5)
        self._ui.cb_duration_streaming_history.addItem("1s", 1)
        self._ui.cb_duration_streaming_history.addItem("2s", 2)
        self._ui.cb_duration_streaming_history.addItem("5s", 5)
        self._ui.cb_duration_streaming_history.addItem("10s", 10)
        self._ui.cb_duration_streaming_history.addItem("20s", 20)
        self._ui.cb_duration_streaming_history.addItem("30s", 30)
        self._ui.cb_duration_streaming_history.addItem("1min", 60)
        self._ui.cb_duration_streaming_history.addItem("2min", 120)
        self._ui.cb_duration_streaming_history.addItem("5min", 300)

    # ==================================================================================================================
    # Slots for Model
    # ==================================================================================================================
    def _on_dwf_version_changed(self, dwf_version):
        self.dev_info.dwf_version = dwf_version
        # self.ad2_settings['DWF Version'] = dwf_version
        # self.update_ad2_settings_list_view()

    # ============== Connected Device Information
    def _on_num_of_connected_devices_changed(self, num_of_connected_devices):
        pass

    def _on_connected_devices_changed(self, connected_devices: list):
        self._ui.cb_device_select.clear()
        for it, dev in enumerate(connected_devices):
            dev: dict
            #  'type': type, 'device_id', 'device_name', 'serial_number'
            self._ui.cb_device_select.addItem(f"{it}: {dev['type']}{dev['device_id']} - {dev['device_name']}")

    # ============== Device information
    def _on_connected_changed(self, connected):
        if connected:
            self.capt_info.lbl_conn_state.setText("Connected")
            self.capt_info.led_conn_state.set_color(color="green")
            self._ui.btn_start_capture.setEnabled(True)
            self._ui.btn_connect.setText("Disconnect")
            self.stream_update_timer.start()
            self.capture_update_timer.start()
        else:
            self.capt_info.lbl_conn_state.setText("Not connected")
            self._ui.btn_connect.setText("Connect")
            self._ui.btn_start_capture.setEnabled(False)
            self._ui.btn_stop.setEnabled(False)
            self.capt_info.led_conn_state.set_color(color="red")

    def _on_device_name_changed(self, device_name):
        self.dev_info.device_name = device_name
        # self.ad2_settings['Device Name'] = device_name
        self.update_ad2_settings_list_view()

    def _on_device_serial_number_changed(self, serial_number):
        self.dev_info.serial_number = serial_number
        # self.ad2_settings['Serial Number'] = serial_number
        self.update_ad2_settings_list_view()

    def _on_device_index_changed(self, device_index):
        pass

    # ============== Acquisition Settings
    def _on_sample_rate_changed(self, sample_rate: int):
        self._ui.sb_acquisition_rate.setRange(1, 1e9)
        self._ui.sb_acquisition_rate.setValue(sample_rate)

    def _on_selected_ain_channel_changed(self, channel):
        self.dev_info.analog_in_channel = channel
        self._ui.cb_channel_select.setCurrentIndex(channel)

    # ============== Analog In Information
    def _on_ain_channels_changed(self, list_of_ad_ins):
        self._ui.cb_channel_select.clear()
        for adin in list_of_ad_ins:
            self._ui.cb_channel_select.addItem(f"Channel {adin}")

    def _on_ain_buffer_size_changed(self, buffer_size):
        pass

    def _on_ain_bits_changed(self, bits):
        pass

    def _on_ain_device_state_changed(self, device_state):
        if device_state == int(DwfStateReady.value):
            self.capt_info.lbl_device_state.setText(f"Ready ({device_state})")
            self.capt_info.led_device_state.set_color(color="green")
            # self.ad2_settings['Device State'] = f"Ready ({device_state})"
        elif device_state == int(DwfStateConfig.value):
            self.capt_info.lbl_device_state.setText(f"Config ({device_state})")
            self.capt_info.led_device_state.set_color(color="yellow")
            # self.ad2_settings['Device State'] = f"Config ({device_state})"
        elif device_state == int(DwfStatePrefill.value):
            self.capt_info.lbl_device_state.setText(f"Prefill ({device_state})")
            self.capt_info.led_device_state.set_color(color="yellow")
        # self.ad2_settings['Device State'] = f"Prefill ({device_state})"
        elif device_state == int(DwfStateArmed.value):
            self.capt_info.lbl_device_state.setText(f"Armed ({device_state})")
            self.capt_info.led_device_state.set_color(color="blue")
        # self.ad2_settings['Device State'] = f"Armed ({device_state})"
        elif device_state == int(DwfStateWait.value):
            self.capt_info.lbl_device_state.setText(f"Wait ({device_state})")
            self.capt_info.led_device_state.set_color(color="red")
            # self.ad2_settings['Device State'] = f"Wait ({device_state})"
        elif device_state == int(DwfStateTriggered.value):
            self.capt_info.lbl_device_state.setText(f"Triggered ({device_state})")
            self.capt_info.led_device_state.set_color(color="green")
            # self.ad2_settings['Device State'] = f"Triggered ({device_state})"
        elif device_state == int(DwfStateRunning.value):
            self.capt_info.lbl_device_state.setText(f"Running ({device_state})")
            self.capt_info.led_device_state.set_color(color="green")
            # self.ad2_settings['Device State'] = f"Running ({device_state})"
        elif device_state == int(DwfStateDone.value):
            self.capt_info.lbl_device_state.setText(f"Done ({device_state})")
            self.capt_info.led_device_state.set_color(color="yellow")
            # self.ad2_settings['Device State'] = f"Done ({device_state})"
        elif device_state == -1:
            self.capt_info.lbl_device_state.setText(f"Disconnected ({device_state})")
            self.capt_info.led_device_state.set_color(color="black")
            # self.ad2_settings['Device State'] = f"Disconnected ({device_state})"
        else:
            self.capt_info.lbl_device_state.setText(f" >>> Unknown ({device_state})")
            self.capt_info.led_device_state.set_color(color="gray")
            # self.ad2_settings['Device State'] = f"Unknown ({device_state})"
        # self.update_ad2_settings_list_view()

    # ============== Analog Out Information
    def _on_aout_channels_changed(self, list_of_ad_outs):
        pass

    # ============== Acquired Signal Information
    def _on_recorded_samples_changed(self, recorded_samples):
        pass
        #print(recorded_samples)
        #self._ui.lcd_captured_samples.display(len(recorded_samples))

    def _on_recording_time_changed(self, recording_time):
        self._ui.lcd_sampled_time.display(recording_time)

    def _on_samples_captured_changed(self, samples_captured):
        self._ui.lcd_captured_samples.display(samples_captured)
        self._ui.lcd_total_captured_samples.display(len(self.model.recorded_samples))

    def _on_samples_lost_changed(self, samples_lost):
        self._ui.lcd_samples_lost.display(samples_lost)

    def _on_samples_corrupted_changed(self, samples_corrupted):
        self._ui.lcd_samples_corrupted.display(samples_corrupted)

    # ============== Recording Flags (starting, stopping and pausing)
    def _on_device_capturing_state_changed(self, capturing):
        if capturing == AD2Constants.CapturingState.RUNNING():
            self.capt_info.led_is_capt.set_color(color="green")
            self.capt_info.lbl_is_capt.setText(AD2Constants.CapturingState.RUNNING(True))
        elif capturing == AD2Constants.CapturingState.PAUSED():
            self.capt_info.led_is_capt.set_color(color="yellow")
            self.capt_info.lbl_is_capt.setText(AD2Constants.CapturingState.PAUSED(True))
        elif capturing == AD2Constants.CapturingState.STOPPED():
            self.capt_info.led_is_capt.set_color(color="red")
            self.capt_info.lbl_is_capt.setText(AD2Constants.CapturingState.STOPPED(True))
        self.update_ad2_settings_list_view()

    def _on_start_recording_changed(self, start_recording):
        self.logger.debug(f"Start Recording: {start_recording}")
        if start_recording:
            self._ui.btn_stop.setEnabled(True)
            self._ui.btn_start_capture.setStyleSheet(CSSPlayPushButton.style_pause())
            self._ui.btn_start_capture.setText("Pause Capture")

    def _on_stop_recording_changed(self, stop_recording):
        self.logger.debug(f"Stop Recording: {stop_recording}")
        if stop_recording:
            self._ui.btn_stop.setEnabled(False)
            self._ui.btn_start_capture.setStyleSheet(CSSPlayPushButton.style_play())
            self._ui.btn_start_capture.setText("Start Capture")

    def _on_pause_recording_changed(self, pause_recording):
        self._ui.btn_stop.setEnabled(True)
        self._ui.btn_start_capture.setStyleSheet(CSSPlayPushButton.style_play())

    def _on_reset_recording_changed(self, reset_recording):
        pass

    # ============== Multiprocessing Information
    def _on_pid_changed(self, pid):
        pass

    # ============== Plotting
    def _on_capture_update_plot(self):

        if len(self.model.recorded_samples) > 0:
            self.scope_captured.clear()
            # print(self.ad2device.recorded_samples)
            d = self.model.recorded_samples[::self.stream_n]
            self.scope_captured.plot(
                x=np.arange(0, len(d))/self.stream_samples_frequency,
                y=d, pen=pg.mkPen(width=1)
            )
            # print(f"Length: {len(self.controller.recorded_sample_stream)}")

        if len(self.controller.status_dqueue) > 0:
            # print(self.controller.status_dqueue)
            self.model.samples_captured = self.controller.status_dqueue[-1]["captured"]
        # self.model.samples_lost = d[1]["lost"]
        # self.model.samples_corrupted = d[1]["corrupted"]
        self._ui.lcd_unconsumed_capture.display(self.model.unconsumed_capture_samples)

    def _on_stream_update_timer_timeout(self):
        self.scope_original.clear()
        # print(self.ad2device.recorded_samples)
        self.scope_original.plot(list(self.controller.data_dqueue)[::self.stream_n], pen=pg.mkPen(width=1))
        self._ui.lcd_unconsumed_stream.display(self.model.unconsumed_stream_samples)


    # ==================================================================================================================
    #
    # ==================================================================================================================
    def on_btn_connect_to_device_clicked(self):
        if self.model.connected:
            self.controller.close_device()
        else:
            try:
                self.controller.connect_device(self._ui.cb_device_select.currentIndex())
                # self.plot_update_timer.setInterval(0.1)
                self.stream_n = int(self.model.sample_rate / self.stream_samples_frequency)
            except Exception as e:
                #    self.status_bar.setStyleSheet('border: 0; color:  red;')
                #    self.status_bar.showMessage(f"Error: {e}")
                self.logger.error(f"Error: {e}")
            self._ui.btn_connect.setText("Disconnect")

    def on_btn_start_capture_clicked(self):
        if self.model.device_capturing_state == AD2Constants.CapturingState.STOPPED() or \
                self.model.device_capturing_state == AD2Constants.CapturingState.PAUSED():
            self.controller.start_capture(clear=self.model.reset_recording)
        elif self.model.device_capturing_state == AD2Constants.CapturingState.RUNNING():
            self.model.reset_recording = False
            self.controller.stop_capture()

    def on_btn_stop_clicked(self):

        self.model.reset_recording = True
        self.controller.stop_capture()
        self._ui.btn_start_capture.setText("Start Capture")
        self._ui.btn_stop.setEnabled(False)
        self._ui.btn_start_capture.setStyleSheet(CSSPlayPushButton.style_play())

        self.capture_update_timer.stop()
        self.scope_captured.clear()
        self.scope_captured.plot(self.model.recorded_samples, pen=pg.mkPen(width=1))

    def closeEvent(self, event):
        super(ControlWindow, self).closeEvent(event)

    def _on_cb_duration_streaming_history_currentIndexChanged(self, index):
        self.model.duration_streaming_history = self._ui.cb_duration_streaming_history.currentData()

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def update_ad2_settings_list_view(self):
        item_model = QStandardItemModel()
        # self.treeview.setModel(item_model)
        # self._populate_model(self.model, self.ad2_settings)

    def _populate_model(self, parent, data):
        """
        Recursively populate QStandardItemModel with YAML data
        """
        if isinstance(data, dict):
            for key, value in data.items():
                item = QStandardItem(str(key))
                parent.appendRow(item)
                self._populate_model(item, value)
        elif isinstance(data, list):
            for value in data:
                item = QStandardItem(str(value))
                parent.appendRow(item)
            # self._populate_model(item, str(data))
        elif isinstance(data, logging.Logger):
            pass
        else:
            item = QStandardItem(str(data))
            parent.appendRow(item)
