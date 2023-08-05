# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mp3monitoring.gui.vertical_tab_bar import VerticalTabWidget


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.setWindowModality(Qt.WindowModal)
        SettingsDialog.resize(711, 497)
        font = QFont()
        font.setFamily(u"Noto Sans")
        SettingsDialog.setFont(font)
        self.gridLayout = QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_box = QDialogButtonBox(SettingsDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.button_box, 1, 0, 1, 1)

        self.tab_widget = VerticalTabWidget(SettingsDialog)
        self.tab_widget.setObjectName(u"tab_widget")
        font1 = QFont()
        font1.setFamily(u"Noto Sans")
        font1.setPointSize(9)
        self.tab_widget.setFont(font1)
        self.tab_widget.setTabPosition(QTabWidget.West)
        self.general = QWidget()
        self.general.setObjectName(u"general")
        font2 = QFont()
        font2.setFamily(u"Noto Sans")
        font2.setPointSize(8)
        self.general.setFont(font2)
        self.gridLayout4 = QGridLayout(self.general)
        self.gridLayout4.setSpacing(7)
        self.gridLayout4.setObjectName(u"gridLayout4")
        self.gridLayout4.setContentsMargins(11, 11, 11, 11)
        self.start_minimized = QCheckBox(self.general)
        self.start_minimized.setObjectName(u"start_minimized")

        self.gridLayout4.addWidget(self.start_minimized, 0, 1, 1, 1)

        self.start_with_system_l = QLabel(self.general)
        self.start_with_system_l.setObjectName(u"start_with_system_l")

        self.gridLayout4.addWidget(self.start_with_system_l, 1, 0, 1, 1)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout4.addItem(self.horizontal_spacer, 0, 2, 1, 1)

        self.start_minimized_l = QLabel(self.general)
        self.start_minimized_l.setObjectName(u"start_minimized_l")

        self.gridLayout4.addWidget(self.start_minimized_l, 0, 0, 1, 1)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout4.addItem(self.vertical_spacer, 2, 0, 1, 1)

        self.start_with_system = QCheckBox(self.general)
        self.start_with_system.setObjectName(u"start_with_system")

        self.gridLayout4.addWidget(self.start_with_system, 1, 1, 1, 1)

        self.tab_widget.addTab(self.general, "")

        self.gridLayout.addWidget(self.tab_widget, 0, 0, 1, 1)


        self.retranslateUi(SettingsDialog)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.start_minimized.setText("")
        self.start_with_system_l.setText(QCoreApplication.translate("SettingsDialog", u"Start with system", None))
        self.start_minimized_l.setText(QCoreApplication.translate("SettingsDialog", u"Start minimized", None))
        self.start_with_system.setText("")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.general), QCoreApplication.translate("SettingsDialog", u"General", None))
    # retranslateUi

