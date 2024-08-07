# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AD2ControlWindowNew.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QToolButton, QWidget)
from . import resources_rc

class Ui_AD2ControlWindowNew(object):
    def setupUi(self, AD2ControlWindowNew):
        if not AD2ControlWindowNew.objectName():
            AD2ControlWindowNew.setObjectName(u"AD2ControlWindowNew")
        AD2ControlWindowNew.resize(629, 813)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaRecord))
        AD2ControlWindowNew.setWindowIcon(icon)
        AD2ControlWindowNew.setStyleSheet(u"")
        self.centralwidget = QWidget(AD2ControlWindowNew)
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
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.grd_information = QGridLayout()
        self.grd_information.setObjectName(u"grd_information")

        self.gridLayout_2.addLayout(self.grd_information, 3, 0, 1, 1)

        self.contentTopBg = QFrame(self.centralwidget)
        self.contentTopBg.setObjectName(u"contentTopBg")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contentTopBg.sizePolicy().hasHeightForWidth())
        self.contentTopBg.setSizePolicy(sizePolicy)
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 16777215))
        self.contentTopBg.setFrameShape(QFrame.Shape.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 10, 0)
        self.vl_header = QFrame(self.contentTopBg)
        self.vl_header.setObjectName(u"vl_header")
        self.vl_header.setEnabled(True)
        sizePolicy.setHeightForWidth(self.vl_header.sizePolicy().hasHeightForWidth())
        self.vl_header.setSizePolicy(sizePolicy)
        self.vl_header.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.vl_header.setFrameShape(QFrame.Shape.NoFrame)
        self.vl_header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.vl_header)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalFrame = QFrame(self.vl_header)
        self.verticalFrame.setObjectName(u"verticalFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.verticalFrame.sizePolicy().hasHeightForWidth())
        self.verticalFrame.setSizePolicy(sizePolicy1)
        self.formLayout = QFormLayout(self.verticalFrame)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(0)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.menuBar = QFrame(self.verticalFrame)
        self.menuBar.setObjectName(u"menuBar")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.menuBar.sizePolicy().hasHeightForWidth())
        self.menuBar.setSizePolicy(sizePolicy2)
        self.menuBar.setMinimumSize(QSize(0, 0))
        self.menuBar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.menuBar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.menuBar)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.menu_file = QToolButton(self.menuBar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_file.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.menu_file.sizePolicy().hasHeightForWidth())
        self.menu_file.setSizePolicy(sizePolicy3)
        self.menu_file.setMinimumSize(QSize(0, 16))
        self.menu_file.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setKerning(True)
        self.menu_file.setFont(font)
        self.menu_file.setMouseTracking(True)
        self.menu_file.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.menu_file.setAutoFillBackground(False)
        self.menu_file.setStyleSheet(u"")
        self.menu_file.setCheckable(False)
        self.menu_file.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menu_file.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.menu_file.setAutoRaise(True)

        self.horizontalLayout_8.addWidget(self.menu_file)

        self.menu_edit = QToolButton(self.menuBar)
        self.menu_edit.setObjectName(u"menu_edit")

        self.horizontalLayout_8.addWidget(self.menu_edit)

        self.menu_run = QToolButton(self.menuBar)
        self.menu_run.setObjectName(u"menu_run")
        self.menu_run.setMinimumSize(QSize(0, 0))
        self.menu_run.setStyleSheet(u"")
        self.menu_run.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menu_run.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.menu_run.setAutoRaise(True)

        self.horizontalLayout_8.addWidget(self.menu_run)


        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.menuBar)

        self.titleRight = QLabel(self.verticalFrame)
        self.titleRight.setObjectName(u"titleRight")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.titleRight.sizePolicy().hasHeightForWidth())
        self.titleRight.setSizePolicy(sizePolicy4)
        self.titleRight.setMaximumSize(QSize(16777215, 45))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleRight.setFont(font1)
        self.titleRight.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.titleRight)


        self.horizontalLayout_7.addWidget(self.verticalFrame)


        self.horizontalLayout_6.addWidget(self.vl_header)

        self.grd_device_connect = QFrame(self.contentTopBg)
        self.grd_device_connect.setObjectName(u"grd_device_connect")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.grd_device_connect.sizePolicy().hasHeightForWidth())
        self.grd_device_connect.setSizePolicy(sizePolicy5)
        self.grd_device_connect.setMinimumSize(QSize(350, 44))
        self.gridLayout_4 = QGridLayout(self.grd_device_connect)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.cb_channel_select = QComboBox(self.grd_device_connect)
        self.cb_channel_select.setObjectName(u"cb_channel_select")
        self.cb_channel_select.setMinimumSize(QSize(0, 22))

        self.gridLayout_4.addWidget(self.cb_channel_select, 2, 3, 1, 1)

        self.sep1 = QFrame(self.grd_device_connect)
        self.sep1.setObjectName(u"sep1")
        self.sep1.setMinimumSize(QSize(0, 0))
        self.sep1.setFrameShape(QFrame.Shape.VLine)
        self.sep1.setFrameShadow(QFrame.Shadow.Plain)

        self.gridLayout_4.addWidget(self.sep1, 2, 0, 2, 1)

        self.cb_device_select = QComboBox(self.grd_device_connect)
        self.cb_device_select.setObjectName(u"cb_device_select")
        self.cb_device_select.setMinimumSize(QSize(200, 22))

        self.gridLayout_4.addWidget(self.cb_device_select, 2, 2, 1, 1)

        self.btn_connect = QPushButton(self.grd_device_connect)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setMinimumSize(QSize(0, 20))

        self.gridLayout_4.addWidget(self.btn_connect, 3, 2, 1, 2)


        self.horizontalLayout_6.addWidget(self.grd_device_connect)


        self.gridLayout_2.addWidget(self.contentTopBg, 0, 0, 1, 1)

        self.grd_controls = QFrame(self.centralwidget)
        self.grd_controls.setObjectName(u"grd_controls")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.grd_controls.sizePolicy().hasHeightForWidth())
        self.grd_controls.setSizePolicy(sizePolicy6)
        self.gridLayout_3 = QGridLayout(self.grd_controls)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lbl_acquisition_rate = QLabel(self.grd_controls)
        self.lbl_acquisition_rate.setObjectName(u"lbl_acquisition_rate")

        self.gridLayout_3.addWidget(self.lbl_acquisition_rate, 0, 1, 1, 1)

        self.sb_acquisition_rate = QSpinBox(self.grd_controls)
        self.sb_acquisition_rate.setObjectName(u"sb_acquisition_rate")
        self.sb_acquisition_rate.setMinimum(1)
        self.sb_acquisition_rate.setMaximum(999999999)

        self.gridLayout_3.addWidget(self.sb_acquisition_rate, 0, 2, 1, 1)

        self.cb_streaming_history = QComboBox(self.grd_controls)
        self.cb_streaming_history.setObjectName(u"cb_streaming_history")

        self.gridLayout_3.addWidget(self.cb_streaming_history, 1, 2, 1, 1)

        self.lbl_streaming_history = QLabel(self.grd_controls)
        self.lbl_streaming_history.setObjectName(u"lbl_streaming_history")

        self.gridLayout_3.addWidget(self.lbl_streaming_history, 1, 1, 1, 1)

        self.horizontalFrame = QFrame(self.grd_controls)
        self.horizontalFrame.setObjectName(u"horizontalFrame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.horizontalFrame.sizePolicy().hasHeightForWidth())
        self.horizontalFrame.setSizePolicy(sizePolicy7)
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_play = QPushButton(self.horizontalFrame)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setEnabled(True)
        self.btn_play.setMinimumSize(QSize(40, 40))
        self.btn_play.setMaximumSize(QSize(40, 40))
        self.btn_play.setStyleSheet(u"/*Play Button*/\n"
"QPushButton {		\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"    border-radius: 0px;\n"
"	text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(47, 104, 57);\n"
"}\n"
"\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(44, 134, 46);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(153, 153, 153);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:checked {	\n"
"	background-color: rgb(49, 89, 62);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/icons-svg/icons-svg/cil-media-play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.btn_play.setIcon(icon1)
        self.btn_play.setIconSize(QSize(20, 20))
        self.btn_play.setCheckable(True)
        self.btn_play.setChecked(False)
        self.btn_play.setAutoExclusive(False)
        self.btn_play.setFlat(False)

        self.horizontalLayout_2.addWidget(self.btn_play)

        self.btn_stop = QPushButton(self.horizontalFrame)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.setMinimumSize(QSize(40, 40))
        self.btn_stop.setMaximumSize(QSize(40, 40))
        self.btn_stop.setStyleSheet(u"/* Stop Button*/\n"
"\n"
"QPushButton {		\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"    border-radius: 0px;\n"
"	text-align: center;\n"
"    icon: url(:/icons-svg/icons-svg/cil-media-stop.svg);\n"
"    icon-size: 16px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(113, 41, 50);\n"
"}\n"
"\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(154, 29, 36);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(153, 153, 153);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u":/icons-svg/icons-svg/cil-media-stop.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_stop.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.btn_stop)

        self.btn_pause = QPushButton(self.horizontalFrame)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setEnabled(False)
        self.btn_pause.setMinimumSize(QSize(40, 40))
        self.btn_pause.setMaximumSize(QSize(40, 40))
        self.btn_pause.setStyleSheet(u"QPushButton {		\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"    border-radius: 0px;\n"
"	text-align: center;\n"
"	icon: url(:/icons-svg/icons-svg/cil-media-pause.svg);\n"
"    icon-size: 16px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(113, 105, 50);\n"
"}\n"
"    \n"
"QPushButton:pressed {	\n"
"    background-color: rgb(154, 136, 36);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"    \n"
"QPushButton:disabled {	\n"
"	background-color: rgb(153, 153, 153);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/icons-svg/icons-svg/cil-media-pause.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_pause.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.btn_pause)

        self.sep2 = QFrame(self.horizontalFrame)
        self.sep2.setObjectName(u"sep2")
        self.sep2.setStyleSheet(u"QFrame[frameShape=\"5\"] /* QFrame::VLine == 0x0005 */\n"
"{\n"
"    color: green;\n"
"    background-color: green;\n"
"}")
        self.sep2.setFrameShape(QFrame.Shape.VLine)
        self.sep2.setFrameShadow(QFrame.Shadow.Plain)

        self.horizontalLayout_2.addWidget(self.sep2)

        self.btn_record = QPushButton(self.horizontalFrame)
        self.btn_record.setObjectName(u"btn_record")
        self.btn_record.setEnabled(False)
        self.btn_record.setMinimumSize(QSize(40, 40))
        self.btn_record.setMaximumSize(QSize(40, 40))
        self.btn_record.setBaseSize(QSize(40, 40))
        self.btn_record.setStyleSheet(u"QPushButton {		\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"    border-radius: 0px;\n"
"	text-align: center;\n"
"	icon: url(:/icons-svg/icons-svg/cil-media-record.svg);\n"
"    icon-size: 16px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(113, 41, 50);\n"
"}\n"
"\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(154, 29, 36);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(153, 153, 153);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:checked {	\n"
"	background-color: rgb(78, 47, 58);\n"
"	icon: url(:/single-color/icons-svg/single_color/cil-media-play.svg);\n"
"   background-color: rgb(183, 0, 0);\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/icons-svg/icons-svg/cil-media-record.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon4.addFile(u":/single-color/icons-svg/single_color/cil-media-play.svg", QSize(), QIcon.Mode.Selected, QIcon.State.On)
        self.btn_record.setIcon(icon4)
        self.btn_record.setCheckable(True)
        self.btn_record.setChecked(False)

        self.horizontalLayout_2.addWidget(self.btn_record)

        self.btn_reset = QPushButton(self.horizontalFrame)
        self.btn_reset.setObjectName(u"btn_reset")
        self.btn_reset.setEnabled(False)
        self.btn_reset.setMinimumSize(QSize(40, 40))
        self.btn_reset.setMaximumSize(QSize(40, 40))
        self.btn_reset.setBaseSize(QSize(40, 40))
        self.btn_reset.setStyleSheet(u"QPushButton {		\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"    border-radius: 0px;\n"
"	text-align: center;\n"
"	icon: url(:/icons-svg/icons-svg/cil-reload.svg);\n"
"    icon-size: 16px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(113, 41, 50);\n"
"}\n"
"\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(154, 29, 36);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	background-color: rgb(153, 153, 153);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.btn_reset)


        self.gridLayout_3.addWidget(self.horizontalFrame, 0, 0, 2, 1)


        self.gridLayout_2.addWidget(self.grd_controls, 2, 0, 1, 1)

        self.grd_plot = QGridLayout()
        self.grd_plot.setObjectName(u"grd_plot")

        self.gridLayout_2.addLayout(self.grd_plot, 4, 0, 1, 1)

        AD2ControlWindowNew.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(AD2ControlWindowNew)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 629, 33))
        AD2ControlWindowNew.setMenuBar(self.menubar)

        self.retranslateUi(AD2ControlWindowNew)

        self.btn_play.setDefault(False)


        QMetaObject.connectSlotsByName(AD2ControlWindowNew)
    # setupUi

    def retranslateUi(self, AD2ControlWindowNew):
        AD2ControlWindowNew.setWindowTitle(QCoreApplication.translate("AD2ControlWindowNew", u"MainWindow", None))
        self.menu_file.setText(QCoreApplication.translate("AD2ControlWindowNew", u"File", None))
        self.menu_edit.setText(QCoreApplication.translate("AD2ControlWindowNew", u"Edit", None))
        self.menu_run.setText(QCoreApplication.translate("AD2ControlWindowNew", u"Run", None))
        self.titleRight.setText(QCoreApplication.translate("AD2ControlWindowNew", u"FlexSensor 6", None))
        self.btn_connect.setText(QCoreApplication.translate("AD2ControlWindowNew", u"Connect", None))
        self.lbl_acquisition_rate.setText(QCoreApplication.translate("AD2ControlWindowNew", u"Acquisition Rate", None))
        self.lbl_streaming_history.setText(QCoreApplication.translate("AD2ControlWindowNew", u"Streaming History", None))
        self.btn_play.setText("")
        self.btn_stop.setText("")
        self.btn_pause.setText("")
        self.btn_record.setText("")
        self.btn_reset.setText("")
    # retranslateUi

