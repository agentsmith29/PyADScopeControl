import logging
import os


import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QStatusBar, QMenu, QToolButton, QMessageBox
from WidgetCollection.Dialogs import AboutDialog

from pyqtgraph.dockarea import DockArea, Dock
from rich.logging import RichHandler

from ADScopeControl.controller.BaseADScopeController import BaseADScopeController
from ADScopeControl.model.AD2ScopeModel import AD2ScopeModel
from ADScopeControl.model.AD2Constants import AD2Constants
from ADScopeControl.view.Ui_AD2ControlWindowNew import Ui_AD2ControlWindowNew
from ADScopeControl.view.widget.WidgetCapturingInformation import WidgetCapturingInformation, WidgetDeviceInformation, \
    WidgetSupervisionInformation
from ADScopeControl import __version__, __description__, __author__, __license__, __url__

from pandasgui import show as pdview

# get the version of the current module, given in the pyproject.toml




class ControlWindow(QMainWindow):

    def __init__(self, model: AD2ScopeModel, controller: BaseADScopeController):
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

        self.setWindowTitle(f'ADScope Control - {__version__}')
        self.setWindowIcon(QIcon(':/icons/icons/adscopecontrol_icon.png'))

        self.about_dialog = AboutDialog(
            "ADScope Control",
            __description__,
            __version__,
            f"2024 {__author__}",
            __url__,
            f"This project is open source and contributions are highly welcome.<br>"
            f"<br>The project is licensed under <br>{__license__}.",
            QPixmap(':/icons/icons/adscopecontrol_icon.png')
        )

        self._init_menu_bar()

        self.capt_info = WidgetCapturingInformation()
        self.dev_info = WidgetDeviceInformation()
        self.supervisor_info = WidgetSupervisionInformation()
        self._ui.grd_information.addWidget(self.capt_info, 0, 0, 1, 1)
        self._ui.grd_information.addWidget(self.supervisor_info, 1, 0, 1, 1)
        self._ui.grd_information.addWidget(self.dev_info, 0, 1, 2, 1)


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

        self.autostop_capture = QTimer()
        self.autostop_capture.setInterval(1000)
        self.autostop_capture.timeout.connect(self.stop_capture_by_timer)

        # Connect the signals and controls
        self._connect_config_properties()
        self._connect_controls()
        self._connect_signals()
        # self._init_other_ui_elements()
        # self._ui.cb_duration_streaming_history.setCurrentIndex(5)

        self._ui.sb_acquisition_rate.setValue(self.model.capturing_information.sample_rate)

    # self._ui.cb_duration_streaming_history.set(self.model.capturing_information.streaming_history)

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def _init_menu_bar(self):
        # Add menu bar
        self.file_menu = QMenu('&Files', self)

        self.act_connect = QAction('Connect', self)
        self.file_menu.addAction(self.act_connect)

        self.file_menu.addSeparator()

        self.act_view_data = QAction('View Data', self)
        self.act_view_data.triggered.connect(self.view_data)
        self.act_view_data.setShortcut('Ctrl+Alt+S')
        self.file_menu.addAction(self.act_view_data)

        self.file_menu.addSeparator()

        self.act_about = QAction('About', self)
        self.act_about.triggered.connect(self.about_dialog.exec)
        self.file_menu.addAction(self.act_about)

        self.act_exit = QAction('Exit', self)
        self.act_exit.setShortcut('Ctrl+Q')
        self.file_menu.addAction(self.act_exit)

        self._ui.menu_file.setMenu(self.file_menu)
        self._ui.menu_file.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

    def view_data(self):
        self.controller.create_dataframe()
        pdview(self.model.capturing_information.recorded_samples_df)

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

    # ==================================================================================================================
    #
    # ==================================================================================================================

    def _connect_config_properties(self):
        # Connect the Controls that are also Settings
        self.model.ad2captdev_config.streaming_history.view.add_new_view(self._ui.cb_streaming_history)
        self.model.ad2captdev_config.sample_rate.view.add_new_view(self._ui.sb_acquisition_rate)
        # Selected Analog In Channel
        self.model.ad2captdev_config.ain_channel.view.add_new_view(self._ui.cb_channel_select)
        #self.model.ad2captdev_config.ain_channel.connect(self._ui_on_selected_ain_changed)

        #self.model.ad2captdev_config.selected_device_index.view.add_new_view(self._ui.cb_device_select)

    def _connect_controls(self):
        self._ui.cb_device_select.currentIndexChanged.connect(self._on_ui_selected_device_index_changed)

        self._ui.btn_connect.clicked.connect(self._on_ui_btn_connect_clicked)

        self._ui.sb_acquisition_rate.valueChanged.connect(self._on_ui_sample_rate_changed)

        # Connect the buttons
        self._ui.btn_play.clicked.connect(
            lambda: self.controller.start_capturing_process()
        )
        self._ui.btn_stop.clicked.connect(self.controller.stop_capturing_process)

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
        self.model.analog_in.signals.selected_ain_channel_changed.connect(self._on_selected_ain_channel_changed)





        # # WaveForms Runtime (DWF) Information
        # # Connected Device Information
        self.model.device_information.signals.device_name_changed.connect(self._on_device_name_changed)
        self.model.device_information.signals.device_serial_number_changed.connect(
            self._on_device_serial_number_changed)
        self.model.capturing_information.signals.ready_for_recording_changed.connect(
            self._on_ready_for_recording_changed)

        # Supervision Information
        self.model.supervisor_information.signals.supervisor_name_changed.connect(self._on_supervisor_name_changed)
        self.model.supervisor_information.signals.supervised_changed.connect(self._on_supervised_changed)
        self.model.supervisor_information.signals.supervisor_model_changed.connect(self._on_supervised_model_changed)



    # ==================================================================================================================
    # Slots
    # ==================================================================================================================
    def _on_supervisor_sweep_start_wavelength_changed(self, sweep_start_wavelength):
        print(f"Sweep Start Wavelength: {sweep_start_wavelength}")

    def _on_supervisor_sweep_end_wavelength_changed(self, sweep_end_wavelength):
        print(f"Sweep End Wavelength: {sweep_end_wavelength}")


    def _on_supervisor_name_changed(self, supervisor_name):
        self.supervisor_info.supervisor_name = supervisor_name

    def _on_supervised_changed(self, supervised):
        self.supervisor_info.supervised = supervised

    def _on_supervised_model_changed(self):
       self.model.supervisor_information.supervisor_model.signals.sweep_start_wavelength_changed.connect(
           self._on_supervisor_sweep_start_wavelength_changed
       )

       self.model.supervisor_information.supervisor_model.signals.sweep_stop_wavelength_changed.connect(
           self._on_supervisor_sweep_end_wavelength_changed

       )

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
        selection_index = self.model.device_information.selected_device_index
        self._ui.cb_device_select.clear()
        for it, dev in enumerate(connected_devices):
            dev: dict
            #  'type': type, 'device_id', 'device_name', 'serial_number'
            self._ui.cb_device_select.addItem(f"{it}: {dev['type']}{dev['device_id']} - {dev['device_name']}")
        self._ui.cb_device_select.setCurrentIndex(selection_index)

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

    # ==================================================================================================================
    # UI Slots
    # ==================================================================================================================
    def _on_ui_selected_device_index_changed(self, index):
        self.controller.set_selected_device(index)

    def _ui_on_selected_ain_changed(self, channel_index):
        """ Gets called if the ui changes the field (should modify the model) """
        self.model.analog_in.selected_ain_channel = channel_index

    def _on_ui_btn_connect_clicked(self):
        if not self.model.device_information.device_connected:
            try:
                self.controller.open_device()
            except Exception as e:
                self.logger.error(f"Error: {e}")
        else:
            self.controller.close_device()

    def _on_ui_sample_rate_changed(self, sample_rate: int):
        self.model.sample_rate = sample_rate

    def _on_model_sample_rate_changed(self, sample_rate: int):
        self._ui.sb_acquisition_rate.setRange(1, 1e9)
        self._ui.sb_acquisition_rate.setValue(sample_rate)

    def stop_capture_by_timer(self):
        self.autostop_capture.start()

        self._ui.btn_record.setChecked(False)
        self.controller.stop_capture()

    def _ui_on_btn_recording_clicked(self):
        if not self.model.capturing_information.device_capturing_state == AD2Constants.CapturingState.RUNNING():
            self.capture_update_timer.setInterval(40)
            self._ui.btn_record.setChecked(True)
            self.controller.start_capture()
            self.autostop_capture.start()
            # spawn a qthread, that automatically stops the recording after a certain time
            self.capture_update_timer.start()
        else:
            self.capture_update_timer.setInterval(1000)
            self._ui.btn_record.setChecked(False)
            self.controller.stop_capture()

            #print("Done")
            #print(len(self.model.capturing_information.recorded_samples_preview))

            #print("Stopped")

    def _ui_on_btn_reset_clicked(self):
        self.scope_captured.clear()
        self.controller.reset_capture()

    # ==================================================================================================================
    # Device information changed
    # ==================================================================================================================
    def _on_selected_ain_channel_changed(self, channel):
        self.controller.set_selected_ain_channel(channel)

    def _on_selected_index_changed(self, index):
        self._ui.cb_channel_select.setCurrentIndex(index)

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
            # To get acceleration, deceleration, etc..
            self.controller.read_supervisor_state()

            # Display a message box
            self.msg_finished_capture = QMessageBox()
            self.msg_finished_capture.setIcon(QMessageBox.Icon.Information)

            self.msg_finished_capture.setText(f"Capture finished! Supervisor Information:\n"
                                              f"Start: {self.model.supervisor_information.sweep_start_wavelength}\n"
                                              f"End: {self.model.supervisor_information.sweep_stop_wavelength}\n"
                                              f"Velocity: {self.model.supervisor_information.velocity}\n"
                                              f"Acceleration: {self.model.supervisor_information.acceleration}\n"
                                              f"Deceleration: {self.model.supervisor_information.deceleration}")

            self.msg_finished_capture.setWindowTitle("Capture finished")
            self.msg_finished_capture.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.msg_finished_capture.show()


    def _on_ready_for_recording_changed(self, ready):
        if ready:
            self.capture_update_timer.start()
            self.stream_update_timer.start()
        else:
            self.capture_update_timer.stop()
            self.stream_update_timer.stop()

    def _on_device_name_changed(self, device_name):
        self.dev_info.device_name = device_name

    def _on_device_serial_number_changed(self, serial_number):
        self.dev_info.serial_number = serial_number

    # ============== Plotting
    def _on_capture_update_plot(self):
        # append to  self.scope_captured
        #self.scope_captured.app

        if self.controller.capture_data_queue.empty() and self.model.capturing_information.stop_recording:
            self.model.capturing_information.recorded_samples_preview.clear()
            for rc in self.model.capturing_information.recorded_samples:
                self.model.capturing_information.recorded_samples_preview.append(rc)

        if len(self.model.capturing_information.recorded_samples) > 0:
            self.scope_captured.clear()
            # print(self.ad2device.recorded_samples)
            d = self.model.capturing_information.recorded_samples_preview

            self.scope_captured.plot(d, pen=pg.mkPen(width=1))
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

    # ============== Connected Device Information
    def _on_num_of_connected_devices_changed(self, num_of_connected_devices):
        pass

    # ============== Acquisition Settings

    def _model_on_selected_ain_changed(self, channel):
        """ Gets called if the model is changed directly (should modify the UI)"""
        self._on_selected_ain_channel_changed(channel)
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

    #def _on_start_recording_changed(self, start_recording):
    #    self.logger.debug(f"Start Recording: {start_recording}")
    #    if start_recording:
    #        self.capture_update_timer.start()
    #        self._ui.btn_stop.setEnabled(True)
    #        # self._ui.btn_start_capture.setStyleSheet(PlayPushButton.style_pause())
    #        self._ui.btn_start_capture.pause()
    #        self._ui.btn_start_capture.setText("Pause Capture")

    #def _on_stop_recording_changed(self, stop_recording):
    #    self.logger.debug(f"Stop Recording: {stop_recording}")
    #    if stop_recording:
    #        self.capture_update_timer.stop()
    #        self._ui.btn_stop.setEnabled(False)
    #        # self._ui.btn_start_capture.setStyleSheet(CSSPlayPushButton.style_play())
    #        self._ui.btn_start_capture.play()
    #        self._ui.btn_start_capture.setText("Start Capture")

    def _on_pause_recording_changed(self, pause_recording):
        self._ui.btn_stop.setEnabled(True)
        # self._ui.btn_start_capture.setStyleSheet(CSSPlayPushButton.style_play())
        self._ui.btn_start_capture.play()

    def _on_reset_recording_changed(self, reset_recording):
        pass

    def closeEvent(self, args):
        self.destroyed.emit()
        self.controller.kill_thread = True
        self.controller.exit()
