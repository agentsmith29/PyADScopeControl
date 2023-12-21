import logging
import os
from collections import deque

import numpy as np

from PySide6.QtCore import QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QStatusBar
from pyqtgraph.dockarea import DockArea, Dock

import pyqtgraph as pg
from rich.logging import RichHandler

from CaptDeviceControl.controller.BaseAD2CaptDevice import BaseAD2CaptDevice
from CaptDeviceControl.model.AD2CaptDeviceModel import AD2CaptDeviceModel
from CaptDeviceControl.model.AD2Constants import AD2Constants
from CaptDeviceControl.view.Ui_AD2ControlWindow import Ui_AD2ControlWindow
from CaptDeviceControl.view.Ui_AD2ControlWindowNew import Ui_AD2ControlWindowNew
from CaptDeviceControl.view.widget.WidgetCapturingInformation import WidgetCapturingInformation, WidgetDeviceInformation

from CaptDeviceControl.constants.dwfconstants import DwfStateReady, DwfStateConfig, DwfStatePrefill, DwfStateArmed, \
    DwfStateWait, \
    DwfStateTriggered, DwfStateRunning, DwfStateDone
from fswidgets import PlayPushButton

from model.submodels.AD2CaptDeviceAnalogInModel import AD2CaptDeviceAnalogInModel
from model.submodels.AD2CaptDeviceCapturingModel import AD2CaptDeviceCapturingModel


class ControlWindow(QMainWindow):

    def __init__(self, model: AD2CaptDeviceModel, controller: BaseAD2CaptDevice):
        super().__init__()
        self.handler = RichHandler(rich_tracebacks=True)
        self.logger = logging.getLogger(f"AD2Window({os.getpid()})")
        self.logger.handlers = [self.handler]
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s %(message)s')
        self.handler.setFormatter(formatter)

        self.controller = controller
        self.model = model

        self._ui = Ui_AD2ControlWindowNew()
        self._ui.setupUi(self)
        # self._ui.btn_start_capture = PlayPushButton(self._ui.btn_start_capture)

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
        self.capture_update_timer.setInterval(10)
        self.capture_update_timer.timeout.connect(self._on_capture_update_plot)

        self.stream_update_timer = QTimer()
        self.stream_update_timer.setInterval(40)
        self.stream_update_timer.timeout.connect(self._on_stream_update_timer_timeout)
        # self.stream_update_timer.start()

        self.stream_samples_frequency = 1000
        self.stream_n = 1

        # Connect the signals and controls
        self._connect_config_properties()
        self._connect_controls()
        self._connect_signals()
        # self._init_other_ui_elements()
        # self._ui.cb_duration_streaming_history.setCurrentIndex(5)

        self.controller.discover_connected_devices()
        self._ui.sb_acquisition_rate.setValue(self.model.capturing_information.sample_rate)
        # self._ui.cb_duration_streaming_history.set(self.model.capturing_information.streaming_history)

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def _add_menues(self):
        pass

    def _connect_config_properties(self):
        # Connect the Controls that are also Settings
        self.model.ad2captdev_config.streaming_history.view.add_new_view(self._ui.cb_streaming_history)

        # Selected Analog IN Channel
        self.model.ad2captdev_config.ain_channel.view.add_new_view(self._ui.cb_channel_select)
        # self.model.ad2captdev_config.ain_channel.connect_property(
        #    self.model.analog_in, AD2CaptDeviceAnalogInModel.selected_ain_channel,
        # )

    def _connect_controls(self):
        self._ui.cb_device_select.currentIndexChanged.connect(self._on_ui_selected_index_changed)

        self._ui.btn_connect.clicked.connect(self._on_ui_btn_connect_clicked)

        self._ui.sb_acquisition_rate.valueChanged.connect(self._on_ui_sample_rate_changed)

        # Connect the buttons
        #self._ui.btn_stop.clicked.connect(self.on_btn_stop_clicked)
        self._ui.btn_play.clicked.connect(
            lambda: self.controller.start_capturing_process(
                self.model.capturing_information.sample_rate,
                self.model.analog_in.selected_ain_channel)
        )
        self._ui.btn_record.clicked.connect(self._ui_on_btn_recording_clicked)
        self._ui.btn_reset.clicked.connect(self._ui_on_btn_reset_clicked)

        # self._ui.cb_channel_select.currentIndexChanged.connect(self._ui_on_selected_ain_changed)

    def _connect_signals(self):
        self.model.signals.dwf_version_changed.connect(self._on_dwf_version_changed)

        self.model.device_information.signals.connected_devices_changed.connect(self._on_connected_devices_changed)
        self.model.device_information.signals.device_state_changed.connect(self._on_device_state_changed)
        self.model.device_information.signals.device_connected_changed.connect(self._on_connected_changed)
        self.model.capturing_information.signals.sample_rate_changed.connect(self._on_model_sample_rate_changed)
        self.model.capturing_information.signals.device_capturing_state_changed.connect(
            self._on_capture_process_state_changed)

        # # WaveForms Runtime (DWF) Information
        # # Connected Device Information
        # self.model.device_information.signals.num_of_connected_devices_changed.connect(self._on_num_of_connected_devices_changed)
        # #self.model.device_information.signals.discovered_devices_changed.connect(self._on_connected_devices_changed)
        # Device information
        self.model.device_information.signals.device_name_changed.connect(self._on_device_name_changed)
        self.model.device_information.signals.device_serial_number_changed.connect(
            self._on_device_serial_number_changed)
        # self.model.device_information.signals.device_index_changed.connect(self._on_device_index_changed)
        # self.model.device_information.selected_device_index_changed.connect(self._on_selected_device_index_changed)
        # # Acquisition Settings
        # self.model.capturing_information.signals.streaming_history.connect(self.)
        # # Analog In Information
        # self.model.analog_in.signals.selected_ain_channel_changed.connect(self._model_on_selected_ain_changed)
        # self.model.analog_in.signals.ain_channels_changed.connect(self._on_ain_channels_changed)
        # self.model.analog_in.signals.ain_buffer_size_changed.connect(self._on_ain_buffer_size_changed)
        # self.model.analog_in.signals.ain_bits_changed.connect(self._on_ain_bits_changed)
        # self.model.analog_in.signals.ain_device_state_changed.connect(self._on_ain_device_state_changed)
        # # Analog Out Information
        # self.model.signals.aout_channels_changed.connect(self._on_aout_channels_changed)
        # # Acquired Signal Information
        # #self.model.signals.recorded_samples_changed.connect(self._on_recorded_samples_changed)
        # #self.model.signals.recording_time_changed.connect(self._on_recording_time_changed)
        # #self.model.signals.samples_captured_changed.connect(self._on_samples_captured_changed)
        # self.model.signals.samples_lost_changed.connect(self._on_samples_lost_changed)
        # self.model.signals.samples_corrupted_changed.connect(self._on_samples_corrupted_changed)
        # # Recording Flags (starting, stopping and pausing)
        # self.model.signals.device_capturing_state_changed.connect(self._on_device_capturing_state_changed)
        # self.model.signals.start_recording_changed.connect(self._on_start_recording_changed)
        # self.model.signals.stop_recording_changed.connect(self._on_stop_recording_changed)
        # self.model.signals.reset_recording_changed.connect(self._on_reset_recording_changed)
        # # Multiprocessing Information
        # self.model.signals.pid_changed.connect(self._on_pid_changed)
        # # Plotting Timer (periodically updating the plot)
        # # self.capture_update_timer.timeout.connect(self._on_capture_update_plot)

    def _on_dwf_version_changed(self, dwf_version):
        """
            Gets called if the DWF version changes. Updates the UI.
            :param dwf_version: The DWF version
        """
        self.dev_info.dwf_version = dwf_version

    def _on_connected_devices_changed(self, connected_devices: list):
        """
        Gets called if the connected devices changed. Populates the combobox with the list of the connected devices.
        :param connected_devices:
        :return:
        """
        self._ui.cb_device_select.clear()
        for it, dev in enumerate(connected_devices):
            dev: dict
            #  'type': type, 'device_id', 'device_name', 'serial_number'
            self._ui.cb_device_select.addItem(f"{it}: {dev['type']}{dev['device_id']} - {dev['device_name']}")
        self._ui.cb_device_select.setCurrentIndex(0)

    def _on_device_state_changed(self, capturing):
        if capturing == AD2Constants.DeviceState.ACQ_NOT_STARTED():
            self.capt_info.led_device_state.set_color(color="yellow")
            self.capt_info.lbl_device_state.setText(AD2Constants.DeviceState.ACQ_NOT_STARTED(True))
        elif capturing == AD2Constants.DeviceState.NO_SAMPLES_AVAILABLE:
            self.capt_info.led_device_state.set_color(color="red")
            self.capt_info.lbl_device_state.setText(AD2Constants.DeviceState.NO_SAMPLES_AVAILABLE(True))
        elif capturing == AD2Constants.DeviceState.SAMPLES_AVAILABLE():
            self.capt_info.led_device_state.set_color(color="green")
            self.capt_info.lbl_device_state.setText(AD2Constants.DeviceState.SAMPLES_AVAILABLE(True))
        elif capturing == AD2Constants.DeviceState.DEV_CAPT_SETUP():
            self.capt_info.led_device_state.set_color(color="yellow")
            self.capt_info.lbl_device_state.setText(AD2Constants.DeviceState.DEV_CAPT_SETUP(True))
            self._ui.btn_pause.setEnabled(True)
            self._ui.btn_stop.setEnabled(True)
            self._ui.btn_record.setEnabled(False)
            self._ui.btn_reset.setEnabled(False)
            self._ui.btn_play.setEnabled(False)
        elif capturing == AD2Constants.DeviceState.DEV_CAPT_STREAMING():
            self.capt_info.led_device_state.set_color(color="green")
            self.capt_info.lbl_device_state.setText(AD2Constants.DeviceState.DEV_CAPT_STREAMING(True))
            self._ui.btn_pause.setEnabled(True)
            self._ui.btn_stop.setEnabled(True)
            self._ui.btn_record.setEnabled(True)
            self._ui.btn_reset.setEnabled(True)
            self._ui.btn_play.setEnabled(True)
            self._ui.btn_play.setChecked(True)
            self.stream_update_timer.start()

    # ==================================================================================================================
    # UI Slots
    # ==================================================================================================================
    def _on_ui_btn_connect_clicked(self):
        if self.model.device_information.device_connected:
            self.controller.close_device()
            self._ui.btn_connect.setText("Connect")
        else:
            try:
                self.controller.open_device(self.model.device_information.selected_device_index)
                self.controller.start_capturing_process(
                    self.model.capturing_information.sample_rate
                )
            except Exception as e:
                self.logger.error(f"Error: {e}")
            self._ui.btn_connect.setText("Disconnect")

    def _on_ui_sample_rate_changed(self, sample_rate: int):
        self.model.sample_rate = sample_rate

    def _on_model_sample_rate_changed(self, sample_rate: int):
        self._ui.sb_acquisition_rate.setRange(1, 1e9)
        self._ui.sb_acquisition_rate.setValue(sample_rate)

    def _ui_on_btn_recording_clicked(self):
        if self._ui.btn_record.isChecked():
            print("Start Recording")
            self.capture_update_timer.start()
            self.controller.start_capture()
        else:
            print("Stop Recording")
            #self._ui.btn_record.setChecked(False)
            self.controller.stop_capture()

    def _ui_on_btn_reset_clicked(self):
        self.controller.reset_capture()

    # ==================================================================================================================
    # Device information changed
    # ==================================================================================================================
    def _on_connected_changed(self, connected):
        if connected:
            self.capt_info.lbl_conn_state.setText("Connected")
            self.capt_info.led_conn_state.set_color(color="green")
            self._ui.btn_pause.setEnabled(False)
            self._ui.btn_stop.setEnabled(False)
            self._ui.btn_record.setEnabled(False)
            self._ui.btn_reset.setEnabled(False)
            self._ui.btn_play.setEnabled(True)
            self._ui.btn_connect.setText("Disconnect")
        else:
            self.capt_info.lbl_conn_state.setText("Not connected")
            self._ui.btn_connect.setText("Connect")
            self._ui.btn_pause.setEnabled(False)
            self._ui.btn_stop.setEnabled(False)
            self._ui.btn_record.setEnabled(False)
            self._ui.btn_reset.setEnabled(False)
            self._ui.btn_play.setEnabled(False)
            self.capt_info.led_conn_state.set_color(color="red")

    # ============== Recording Flags (starting, stopping and pausing)
    def _on_capture_process_state_changed(self, capturing):
        if capturing == AD2Constants.CapturingState.RUNNING():
            self.capt_info.led_is_capt.set_color(color="green")
            self.capt_info.lbl_is_capt.setText(AD2Constants.CapturingState.RUNNING(True))
            self._ui.btn_record.setChecked(True)
        elif capturing == AD2Constants.CapturingState.PAUSED():
            self.capt_info.led_is_capt.set_color(color="yellow")
            self.capt_info.lbl_is_capt.setText(AD2Constants.CapturingState.PAUSED(True))
        elif capturing == AD2Constants.CapturingState.STOPPED():
            self.capt_info.led_is_capt.set_color(color="red")
            self.capt_info.lbl_is_capt.setText(AD2Constants.CapturingState.STOPPED(True))
            self._ui.btn_record.setChecked(False)




























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

    # def _init_other_ui_elements(self):
    #    self._ui.cb_duration_streaming_history.addItem("100ms", 0.1)
    #    self._ui.cb_duration_streaming_history.addItem("200ms", 0.2)
    #    self._ui.cb_duration_streaming_history.addItem("500ms", 0.5)
    #    self._ui.cb_duration_streaming_history.addItem("1s", 1)
    #    self._ui.cb_duration_streaming_history.addItem("2s", 2)
    #   self._ui.cb_duration_streaming_history.addItem("5s", 5)
    ##   self._ui.cb_duration_streaming_history.addItem("10s", 10)
    #   self._ui.cb_duration_streaming_history.addItem("20s", 20)
    #   self._ui.cb_duration_streaming_history.addItem("30s", 30)
    #   self._ui.cb_duration_streaming_history.addItem("1min", 60)
    #   self._ui.cb_duration_streaming_history.addItem("2min", 120)
    #  self._ui.cb_duration_streaming_history.addItem("5min", 300)

    # ==================================================================================================================
    # Slots for Model
    # ==================================================================================================================
    def _on_ui_selected_index_changed(self, index):
        self.controller.selected_device_index(index)
        # self.controller.device_selected_index_changed()
        # self.controller.mpcaptdevicecontrol.selected_device_index(index)
        # First populate the AIn box+
        # m: dict = self.model.connected_devices[index]
        # self.model.ain_channels = list(range(0, int(m['analog_in_channels'])))

    # ============== Connected Device Information
    def _on_num_of_connected_devices_changed(self, num_of_connected_devices):
        pass

    def _on_device_name_changed(self, device_name):
        self.dev_info.device_name = device_name
        # self.ad2_settings['Device Name'] = device_name
        self.update_ad2_settings_list_view()

    def _on_device_serial_number_changed(self, serial_number):
        self.dev_info.serial_number = serial_number
        # self.ad2_settings['Serial Number'] = serial_number
        self.update_ad2_settings_list_view()

    # ============== Acquisition Settings

    def _model_on_selected_ain_changed(self, channel):
        """ Gets called if the model is changed directly (should modify the UI)"""
        self._on_selected_ain_channel_changed(channel)
        self._ui.cb_channel_select.setCurrentIndex(channel)

    def _ui_on_selected_ain_changed(self, channel):
        """ Gets called if the ui changes the field (should modify the model) """
        self._on_selected_ain_channel_changed(channel)
        self.model.selected_ain_channel = channel

    def _on_selected_ain_channel_changed(self, channel):
        self.dev_info.analog_in_channel = channel

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
        # print(recorded_samples)
        # self._ui.lcd_captured_samples.display(len(recorded_samples))

    def _on_recording_time_changed(self, recording_time):
        self._ui.lcd_sampled_time.display(recording_time)

    def _on_samples_captured_changed(self, samples_captured):
        self._ui.lcd_captured_samples.display(samples_captured)
        self._ui.lcd_total_captured_samples.display(len(self.model.recorded_samples))

    def _on_samples_lost_changed(self, samples_lost):
        self._ui.lcd_samples_lost.display(samples_lost)

    def _on_samples_corrupted_changed(self, samples_corrupted):
        self._ui.lcd_samples_corrupted.display(samples_corrupted)

    def _on_start_recording_changed(self, start_recording):
        self.logger.debug(f"Start Recording: {start_recording}")
        if start_recording:
            self._ui.btn_stop.setEnabled(True)
            # self._ui.btn_start_capture.setStyleSheet(PlayPushButton.style_pause())
            self._ui.btn_start_capture.pause()
            self._ui.btn_start_capture.setText("Pause Capture")

    def _on_stop_recording_changed(self, stop_recording):
        self.logger.debug(f"Stop Recording: {stop_recording}")
        if stop_recording:
            self._ui.btn_stop.setEnabled(False)
            # self._ui.btn_start_capture.setStyleSheet(CSSPlayPushButton.style_play())
            self._ui.btn_start_capture.play()
            self._ui.btn_start_capture.setText("Start Capture")

    def _on_pause_recording_changed(self, pause_recording):
        self._ui.btn_stop.setEnabled(True)
        # self._ui.btn_start_capture.setStyleSheet(CSSPlayPushButton.style_play())
        self._ui.btn_start_capture.play()

    def _on_reset_recording_changed(self, reset_recording):
        pass

    # ============== Multiprocessing Information
    def _on_pid_changed(self, pid):
        pass

    # ============== Plotting
    def _on_capture_update_plot(self):

        if len(self.model.capturing_information.recorded_samples) > 0:
            self.scope_captured.clear()
            # print(self.ad2device.recorded_samples)
            d = self.model.capturing_information.recorded_samples[::self.stream_n]
            self.scope_captured.plot(
                x=np.arange(0, len(d)) / self.stream_samples_frequency,
                y=d, pen=pg.mkPen(width=1)
            )
            # print(f"Length: {len(self.controller.recorded_sample_stream)}")

        #if len(self.controller.status_dqueue) > 0:
            # print(self.controller.status_dqueue)
        #    self.model.samples_captured = self.controller.status_dqueue[-1]["captured"]
        # self.model.samples_lost = d[1]["lost"]
        # self.model.samples_corrupted = d[1]["corrupted"]
        #self._ui.lcd_unconsumed_capture.display(self.model.unconsumed_capture_samples)

    def _on_stream_update_timer_timeout(self):
        self.scope_original.clear()
        # print(self.ad2device.recorded_samples)

        self.scope_original.plot(
            np.array(self.controller.streaming_dqueue),  # [::100],
            pen=pg.mkPen(width=1))
        # self._ui.lcd_unconsumed_stream.display(self.model.capturing_information.unconsumed_stream_samples)

    # ==================================================================================================================
    #
    # ==================================================================================================================


    def closeEvent(self, event):
        super(ControlWindow, self).closeEvent(event)

    # def _on_cb_duration_streaming_history_currentIndexChanged(self, index):#
    # self.model.duration_streaming_history = self._ui.cb_duration_streaming_history.currentData()
    # self.controller.streaming_dqueue = deque(
    #    maxlen=int(
    #        self.model.duration_streaming_history *
    #        self.model.capturing_information.streaming_history))

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

    def closeEvent(self, args):
        print("Destroyed")
        self.controller.exit()
        self.destroyed.emit()
