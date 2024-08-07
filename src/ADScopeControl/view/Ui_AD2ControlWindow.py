# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AD2ControlWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QLCDNumber, QLabel, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

from fswidgets import PlayPushButton
from . import resources_rc

class Ui_AD2ControlWindow(object):
    def setupUi(self, AD2ControlWindow):
        if not AD2ControlWindow.objectName():
            AD2ControlWindow.setObjectName(u"AD2ControlWindow")
        AD2ControlWindow.resize(646, 765)
        AD2ControlWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(AD2ControlWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"QWidget{\n"
"    background-color: rgb(40, 44, 52);\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Q"
                        "TableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::se"
                        "ction:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizo"
                        "ntal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-r"
                        "adius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     he"
                        "ight: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* ///////////////////////////////////////////////////////////"
                        "//////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(52, 59, 72);\n"
"	border-radius: 2px;\n"
"	border: 1px solid rgb(0, 0, 0);\n"
"}\n"
"QComboBox:hover{\n"
"	border: 1px solid rgb(42, 175, 211);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 2px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius"
                        ": 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"/*QComboBox QAbstractItemView::item {\n"
"  min-height: 150px;\n"
"}*/\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(0, 0, 0);\n"
"    border: 1px solid rgb(42, 175, 211);\n"
"    height: 10px;\n"
"    width: 8px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider"
                        "::handle:horizontal:hover {\n"
"    background-color: rgb(42, 141, 211);\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(42, 141, 211);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
""
                        "QCommandLinkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"QPushButton {\n"
"	border: 1px solid rgb(42, 175, 211);\n"
"	border-radius: 2px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 1px solid rgb(42, 141, 211);\n"
"    border-radius: 2px;	\n"
"	background-color: rgb(42, 141, 211);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 1px solid rgb(42, 141, 211);\n"
"    border-radius: 2px;	\n"
"	background-color: rgb(35, 40, 49);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"/* QMenu ------------------------------------------------------------------"
                        "\n"
"\n"
"examples: https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qmenu\n"
"\n"
"--------------------------------------------------------------------------- */\n"
"QMenu {\n"
"    background-color: rgb(40, 44, 52);\n"
"    margin: 2px; /* some spacing around the menu */\n"
"}\n"
"\n"
"QMenu::item {\n"
"    padding: 2px 25px 2px 20px;\n"
"    border: 1px solid transparent; /* reserve space for selection border */\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    border-color: darkblue;\n"
"    background: rgba(100, 100, 100, 150);\n"
"}\n"
"\n"
"QMenu::icon:checked { /* appearance of a 'checked' icon */\n"
"    background: gray;\n"
"    border: 1px inset gray;\n"
"    position: absolute;\n"
"    top: 1px;\n"
"    right: 1px;\n"
"    bottom: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"    height: 2px;\n"
"    background: lightblue;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"}\n"
"\n"
"QTabWidge"
                        "t::pane {\n"
"  border: 1px solid lightgray;\n"
"  top:-1px; \n"
"  background:  rgb(40, 44, 52); \n"
"} \n"
"\n"
"QTabBar::tab {\n"
"  background: rgb(40, 44, 52);; \n"
"  border: 1px solid lightgray; \n"
"  padding: 2px;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"} \n"
"\n"
"QTabBar::tab:selected { \n"
"  background:  rgb(189, 147, 249);\n"
"  margin-bottom: -1px; \n"
"}\n"
"")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout_3 = QGridLayout(self.widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridFrame_2 = QFrame(self.widget)
        self.gridFrame_2.setObjectName(u"gridFrame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridFrame_2.sizePolicy().hasHeightForWidth())
        self.gridFrame_2.setSizePolicy(sizePolicy)
        self.grd_capturing_information = QGridLayout(self.gridFrame_2)
        self.grd_capturing_information.setObjectName(u"grd_capturing_information")
        self.grd_capturing_information.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.frame = QFrame(self.gridFrame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.HLine)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.frame.setLineWidth(5)

        self.grd_capturing_information.addWidget(self.frame, 6, 0, 1, 4)

        self.frame_2 = QFrame(self.gridFrame_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.HLine)
        self.frame_2.setFrameShadow(QFrame.Sunken)

        self.grd_capturing_information.addWidget(self.frame_2, 2, 0, 1, 4)

        self.groupBox_2 = QGroupBox(self.gridFrame_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 0))
        self.gridLayout_10 = QGridLayout(self.groupBox_2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(-1, 3, -1, 5)
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.lcd_unconsumed_capture = QLCDNumber(self.groupBox_2)
        self.lcd_unconsumed_capture.setObjectName(u"lcd_unconsumed_capture")
        self.lcd_unconsumed_capture.setMinimumSize(QSize(0, 20))
        self.lcd_unconsumed_capture.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_9.addWidget(self.lcd_unconsumed_capture, 2, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_9.addWidget(self.label_4, 0, 0, 1, 1)

        self.lcd_samples_corrupted = QLCDNumber(self.groupBox_2)
        self.lcd_samples_corrupted.setObjectName(u"lcd_samples_corrupted")
        self.lcd_samples_corrupted.setMaximumSize(QSize(16777215, 20))
        self.lcd_samples_corrupted.setFrameShadow(QFrame.Sunken)
        self.lcd_samples_corrupted.setSegmentStyle(QLCDNumber.Filled)

        self.gridLayout_9.addWidget(self.lcd_samples_corrupted, 0, 3, 1, 1)

        self.lcd_samples_lost = QLCDNumber(self.groupBox_2)
        self.lcd_samples_lost.setObjectName(u"lcd_samples_lost")
        self.lcd_samples_lost.setMaximumSize(QSize(16777215, 20))
        self.lcd_samples_lost.setFrameShadow(QFrame.Sunken)
        self.lcd_samples_lost.setSegmentStyle(QLCDNumber.Filled)

        self.gridLayout_9.addWidget(self.lcd_samples_lost, 0, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_9.addWidget(self.label_5, 0, 2, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_9.addWidget(self.label_8, 2, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_9.addWidget(self.label_9, 2, 2, 1, 1)

        self.lcd_unconsumed_stream = QLCDNumber(self.groupBox_2)
        self.lcd_unconsumed_stream.setObjectName(u"lcd_unconsumed_stream")
        self.lcd_unconsumed_stream.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_9.addWidget(self.lcd_unconsumed_stream, 2, 3, 1, 1)

        self.frame_3 = QFrame(self.groupBox_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.HLine)
        self.frame_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_9.addWidget(self.frame_3, 1, 0, 1, 4)


        self.gridLayout_10.addLayout(self.gridLayout_9, 0, 0, 1, 1)


        self.grd_capturing_information.addWidget(self.groupBox_2, 3, 0, 1, 4)

        self.lcd_captured_samples = QLCDNumber(self.gridFrame_2)
        self.lcd_captured_samples.setObjectName(u"lcd_captured_samples")
        self.lcd_captured_samples.setMaximumSize(QSize(16777215, 16777215))
        self.lcd_captured_samples.setFrameShadow(QFrame.Sunken)
        self.lcd_captured_samples.setLineWidth(1)
        self.lcd_captured_samples.setMidLineWidth(0)
        self.lcd_captured_samples.setDigitCount(25)
        self.lcd_captured_samples.setSegmentStyle(QLCDNumber.Filled)

        self.grd_capturing_information.addWidget(self.lcd_captured_samples, 0, 1, 1, 1)

        self.label_2 = QLabel(self.gridFrame_2)
        self.label_2.setObjectName(u"label_2")

        self.grd_capturing_information.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_10 = QLabel(self.gridFrame_2)
        self.label_10.setObjectName(u"label_10")

        self.grd_capturing_information.addWidget(self.label_10, 1, 0, 1, 1)

        self.lcd_total_captured_samples = QLCDNumber(self.gridFrame_2)
        self.lcd_total_captured_samples.setObjectName(u"lcd_total_captured_samples")
        self.lcd_total_captured_samples.setDigitCount(25)
        self.lcd_total_captured_samples.setProperty("value", 99999.000000000000000)

        self.grd_capturing_information.addWidget(self.lcd_total_captured_samples, 1, 1, 1, 1)

        self.label_3 = QLabel(self.gridFrame_2)
        self.label_3.setObjectName(u"label_3")

        self.grd_capturing_information.addWidget(self.label_3, 0, 2, 2, 1)

        self.lcd_sampled_time = QLCDNumber(self.gridFrame_2)
        self.lcd_sampled_time.setObjectName(u"lcd_sampled_time")
        self.lcd_sampled_time.setMaximumSize(QSize(16777215, 32))
        self.lcd_sampled_time.setFrameShadow(QFrame.Sunken)
        self.lcd_sampled_time.setDigitCount(6)
        self.lcd_sampled_time.setMode(QLCDNumber.Dec)
        self.lcd_sampled_time.setSegmentStyle(QLCDNumber.Filled)
        self.lcd_sampled_time.setProperty("value", 1.423521000000000)

        self.grd_capturing_information.addWidget(self.lcd_sampled_time, 0, 3, 2, 1)


        self.gridLayout_2.addWidget(self.gridFrame_2, 6, 0, 1, 4)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 2)

        self.grd_plot = QGridLayout()
        self.grd_plot.setObjectName(u"grd_plot")

        self.gridLayout_2.addLayout(self.grd_plot, 7, 0, 1, 4)

        self.lbl_hz_acquisition = QLabel(self.widget)
        self.lbl_hz_acquisition.setObjectName(u"lbl_hz_acquisition")

        self.gridLayout_2.addWidget(self.lbl_hz_acquisition, 2, 0, 1, 2)

        self.cb_device_select = QComboBox(self.widget)
        self.cb_device_select.setObjectName(u"cb_device_select")

        self.gridLayout_2.addWidget(self.cb_device_select, 1, 0, 1, 2)

        self.grd_information = QGridLayout()
        self.grd_information.setObjectName(u"grd_information")

        self.gridLayout_2.addLayout(self.grd_information, 5, 1, 1, 3)

        self.btn_connect = QPushButton(self.widget)
        self.btn_connect.setObjectName(u"btn_connect")

        self.gridLayout_2.addWidget(self.btn_connect, 1, 3, 1, 1)

        self.cb_duration_streaming_history = QComboBox(self.widget)
        self.cb_duration_streaming_history.setObjectName(u"cb_duration_streaming_history")

        self.gridLayout_2.addWidget(self.cb_duration_streaming_history, 3, 2, 1, 2)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 2, 1, 1)

        self.sb_acquisition_rate = QSpinBox(self.widget)
        self.sb_acquisition_rate.setObjectName(u"sb_acquisition_rate")
        self.sb_acquisition_rate.setMinimum(1)
        self.sb_acquisition_rate.setMaximum(999999999)

        self.gridLayout_2.addWidget(self.sb_acquisition_rate, 2, 2, 1, 2)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.verticalFrame = QFrame(self.widget)
        self.verticalFrame.setObjectName(u"verticalFrame")
        sizePolicy.setHeightForWidth(self.verticalFrame.sizePolicy().hasHeightForWidth())
        self.verticalFrame.setSizePolicy(sizePolicy)
        self.verticalFrame.setMinimumSize(QSize(60, 0))
        self.verticalFrame.setMaximumSize(QSize(60, 16777215))
        self.gridLayout_4 = QGridLayout(self.verticalFrame)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalFrame_1 = QFrame(self.verticalFrame)
        self.verticalFrame_1.setObjectName(u"verticalFrame_1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.verticalFrame_1.sizePolicy().hasHeightForWidth())
        self.verticalFrame_1.setSizePolicy(sizePolicy1)
        self.verticalFrame_1.setMinimumSize(QSize(60, 0))
        self.verticalFrame_1.setMaximumSize(QSize(60, 16777215))
        self.verticalLayout = QVBoxLayout(self.verticalFrame_1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_start_capture = PlayPushButton(self.verticalFrame_1)
        self.btn_start_capture.setObjectName(u"btn_start_capture")
        self.btn_start_capture.setEnabled(False)
        self.btn_start_capture.setMinimumSize(QSize(60, 60))
        self.btn_start_capture.setMaximumSize(QSize(60, 60))
        self.btn_start_capture.setStyleSheet(u"QPushButton {		\n"
"   background-color: rgb(36, 209, 21);\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"    border-radius: 0px;\n"
"	border-left: 22px solid transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"    background-image: url(:/icons/icons/cil-media-play.png);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(26, 153, 16);\n"
"}\n"
"\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(20, 120, 12);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(153, 153, 153);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.btn_start_capture)

        self.btn_stop = PlayPushButton(self.verticalFrame_1)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.setMinimumSize(QSize(60, 60))
        self.btn_stop.setMaximumSize(QSize(60, 60))
        self.btn_stop.setStyleSheet(u"QPushButton {		\n"
"   background-color: rgb(242, 41, 41);\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"    border-radius: 0px;\n"
"	border-left: 22px solid transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"    background-image: url(:/icons/icons/cil-media-stop.png)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(235, 64, 52);\n"
"}\n"
"\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(201, 17, 4);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(153, 153, 153);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.btn_stop)


        self.gridLayout_4.addWidget(self.verticalFrame_1, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.verticalFrame, 5, 0, 1, 1)

        self.cb_channel_select = QComboBox(self.widget)
        self.cb_channel_select.setObjectName(u"cb_channel_select")

        self.gridLayout_2.addWidget(self.cb_channel_select, 1, 2, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        AD2ControlWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(AD2ControlWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 646, 22))
        AD2ControlWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(AD2ControlWindow)
        self.statusbar.setObjectName(u"statusbar")
        AD2ControlWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AD2ControlWindow)

        QMetaObject.connectSlotsByName(AD2ControlWindow)
    # setupUi

    def retranslateUi(self, AD2ControlWindow):
        AD2ControlWindow.setWindowTitle(QCoreApplication.translate("AD2ControlWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("AD2ControlWindow", u"AD2 Sample Information", None))
        self.label_4.setText(QCoreApplication.translate("AD2ControlWindow", u"Samples lost", None))
        self.label_5.setText(QCoreApplication.translate("AD2ControlWindow", u"Samples corrupted", None))
        self.label_8.setText(QCoreApplication.translate("AD2ControlWindow", u"Uncons. Capture", None))
        self.label_9.setText(QCoreApplication.translate("AD2ControlWindow", u"Uncons. Stream", None))
        self.label_2.setText(QCoreApplication.translate("AD2ControlWindow", u"Current Captured Samples", None))
        self.label_10.setText(QCoreApplication.translate("AD2ControlWindow", u"Total Captured Samples", None))
        self.label_3.setText(QCoreApplication.translate("AD2ControlWindow", u"Sampled Time (s)", None))
        self.label.setText(QCoreApplication.translate("AD2ControlWindow", u"History", None))
        self.lbl_hz_acquisition.setText(QCoreApplication.translate("AD2ControlWindow", u"Acquisition Rate", None))
        self.btn_connect.setText(QCoreApplication.translate("AD2ControlWindow", u"Connect", None))
        self.label_7.setText(QCoreApplication.translate("AD2ControlWindow", u"Channel", None))
        self.sb_acquisition_rate.setSuffix(QCoreApplication.translate("AD2ControlWindow", u" Hz", None))
        self.label_6.setText(QCoreApplication.translate("AD2ControlWindow", u"Device", None))
        self.btn_start_capture.setText(QCoreApplication.translate("AD2ControlWindow", u"Start Capture", None))
        self.btn_stop.setText(QCoreApplication.translate("AD2ControlWindow", u"PushButton", None))
    # retranslateUi

