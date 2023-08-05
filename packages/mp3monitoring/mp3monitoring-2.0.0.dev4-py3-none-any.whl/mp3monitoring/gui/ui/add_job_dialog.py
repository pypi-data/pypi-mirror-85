# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_job_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AddJobDialog(object):
    def setupUi(self, AddJobDialog):
        if not AddJobDialog.objectName():
            AddJobDialog.setObjectName(u"AddJobDialog")
        AddJobDialog.resize(648, 220)
        font = QFont()
        font.setFamily(u"Noto Sans")
        AddJobDialog.setFont(font)
        self.gridLayout = QGridLayout(AddJobDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName(u"horizontal_layout")
        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontal_layout.addItem(self.horizontal_spacer)

        self.add_button = QPushButton(AddJobDialog)
        self.add_button.setObjectName(u"add_button")
        self.add_button.setEnabled(False)

        self.horizontal_layout.addWidget(self.add_button)

        self.add_and_start_button = QPushButton(AddJobDialog)
        self.add_and_start_button.setObjectName(u"add_and_start_button")
        self.add_and_start_button.setEnabled(False)

        self.horizontal_layout.addWidget(self.add_and_start_button)

        self.cancel_button = QPushButton(AddJobDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.horizontal_layout.addWidget(self.cancel_button)


        self.gridLayout.addLayout(self.horizontal_layout, 11, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.target_label = QLabel(AddJobDialog)
        self.target_label.setObjectName(u"target_label")

        self.gridLayout_2.addWidget(self.target_label, 1, 0, 1, 1)

        self.recursive_search = QCheckBox(AddJobDialog)
        self.recursive_search.setObjectName(u"recursive_search")
        self.recursive_search.setLayoutDirection(Qt.LeftToRight)
        self.recursive_search.setChecked(True)

        self.gridLayout_2.addWidget(self.recursive_search, 2, 2, 1, 1)

        self.interval_label = QLabel(AddJobDialog)
        self.interval_label.setObjectName(u"interval_label")

        self.gridLayout_2.addWidget(self.interval_label, 4, 0, 1, 1)

        self.source_label = QLabel(AddJobDialog)
        self.source_label.setObjectName(u"source_label")

        self.gridLayout_2.addWidget(self.source_label, 0, 0, 1, 1)

        self.horizontal_layout_5 = QHBoxLayout()
        self.horizontal_layout_5.setObjectName(u"horizontal_layout_5")
        self.target_dir = QLineEdit(AddJobDialog)
        self.target_dir.setObjectName(u"target_dir")

        self.horizontal_layout_5.addWidget(self.target_dir)

        self.target_dialog_button = QToolButton(AddJobDialog)
        self.target_dialog_button.setObjectName(u"target_dialog_button")

        self.horizontal_layout_5.addWidget(self.target_dialog_button)


        self.gridLayout_2.addLayout(self.horizontal_layout_5, 1, 2, 1, 1)

        self.run_at_startup = QCheckBox(AddJobDialog)
        self.run_at_startup.setObjectName(u"run_at_startup")
        self.run_at_startup.setChecked(True)

        self.gridLayout_2.addWidget(self.run_at_startup, 3, 2, 1, 1)

        self.recursive_label = QLabel(AddJobDialog)
        self.recursive_label.setObjectName(u"recursive_label")
        self.recursive_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.recursive_label, 2, 0, 1, 1)

        self.horizontal_layout_4 = QHBoxLayout()
        self.horizontal_layout_4.setObjectName(u"horizontal_layout_4")
        self.source_dir = QLineEdit(AddJobDialog)
        self.source_dir.setObjectName(u"source_dir")

        self.horizontal_layout_4.addWidget(self.source_dir)

        self.source_dialog_button = QToolButton(AddJobDialog)
        self.source_dialog_button.setObjectName(u"source_dialog_button")

        self.horizontal_layout_4.addWidget(self.source_dialog_button)


        self.gridLayout_2.addLayout(self.horizontal_layout_4, 0, 2, 1, 1)

        self.run_at_startup_label = QLabel(AddJobDialog)
        self.run_at_startup_label.setObjectName(u"run_at_startup_label")

        self.gridLayout_2.addWidget(self.run_at_startup_label, 3, 0, 1, 1)

        self.horizontal_layout_6 = QHBoxLayout()
        self.horizontal_layout_6.setObjectName(u"horizontal_layout_6")
        self.sleep_time = QTimeEdit(AddJobDialog)
        self.sleep_time.setObjectName(u"sleep_time")
        self.sleep_time.setWrapping(False)
        self.sleep_time.setMaximumTime(QTime(1, 0, 0))
        self.sleep_time.setCurrentSection(QDateTimeEdit.MinuteSection)
        self.sleep_time.setTime(QTime(0, 0, 10))

        self.horizontal_layout_6.addWidget(self.sleep_time)

        self.horizontal_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontal_layout_6.addItem(self.horizontal_spacer_2)


        self.gridLayout_2.addLayout(self.horizontal_layout_6, 4, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 3, 0, 2, 1)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.vertical_spacer, 10, 0, 1, 1)

        self.line = QFrame(AddJobDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 5, 0, 1, 1)


        self.retranslateUi(AddJobDialog)

        QMetaObject.connectSlotsByName(AddJobDialog)
    # setupUi

    def retranslateUi(self, AddJobDialog):
        AddJobDialog.setWindowTitle(QCoreApplication.translate("AddJobDialog", u"Dialog", None))
        self.add_button.setText(QCoreApplication.translate("AddJobDialog", u"Add", None))
        self.add_and_start_button.setText(QCoreApplication.translate("AddJobDialog", u"Add && Start", None))
        self.cancel_button.setText(QCoreApplication.translate("AddJobDialog", u"Cancel", None))
        self.target_label.setText(QCoreApplication.translate("AddJobDialog", u"Target Directory", None))
        self.recursive_search.setText("")
        self.interval_label.setText(QCoreApplication.translate("AddJobDialog", u"Intervall (mm:ss)", None))
        self.source_label.setText(QCoreApplication.translate("AddJobDialog", u"Source Directory", None))
        self.target_dialog_button.setText(QCoreApplication.translate("AddJobDialog", u"...", None))
        self.run_at_startup.setText("")
#if QT_CONFIG(tooltip)
        self.recursive_label.setToolTip(QCoreApplication.translate("AddJobDialog", u"Checks folder recursive.", None))
#endif // QT_CONFIG(tooltip)
        self.recursive_label.setText(QCoreApplication.translate("AddJobDialog", u"Recursive", None))
        self.source_dialog_button.setText(QCoreApplication.translate("AddJobDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.run_at_startup_label.setToolTip(QCoreApplication.translate("AddJobDialog", u"Run this job at program start.", None))
#endif // QT_CONFIG(tooltip)
        self.run_at_startup_label.setText(QCoreApplication.translate("AddJobDialog", u"Run at Startup", None))
        self.sleep_time.setSpecialValueText("")
        self.sleep_time.setDisplayFormat(QCoreApplication.translate("AddJobDialog", u"mm:ss", None))
    # retranslateUi

