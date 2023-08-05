# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shutdown_overlay.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mp3monitoring.gui.widget.wait_animation import WaitAnimation


class Ui_ShutdownOverlay(object):
    def setupUi(self, ShutdownOverlay):
        if not ShutdownOverlay.objectName():
            ShutdownOverlay.setObjectName(u"ShutdownOverlay")
        ShutdownOverlay.resize(598, 379)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ShutdownOverlay.sizePolicy().hasHeightForWidth())
        ShutdownOverlay.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Noto Sans")
        ShutdownOverlay.setFont(font)
        ShutdownOverlay.setWindowOpacity(1.000000000000000)
        ShutdownOverlay.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(ShutdownOverlay)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.vertical_spacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.vertical_spacer_3)

        self.spin_animation = WaitAnimation(ShutdownOverlay)
        self.spin_animation.setObjectName(u"spin_animation")
        sizePolicy.setHeightForWidth(self.spin_animation.sizePolicy().hasHeightForWidth())
        self.spin_animation.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.spin_animation)
        self.gridLayout.setObjectName(u"gridLayout")

        self.verticalLayout.addWidget(self.spin_animation)

        self.vertical_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.vertical_spacer)

        self.message = QLabel(ShutdownOverlay)
        self.message.setObjectName(u"message")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.message.sizePolicy().hasHeightForWidth())
        self.message.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamily(u"Noto Sans")
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setWeight(75)
        self.message.setFont(font1)
        self.message.setLayoutDirection(Qt.LeftToRight)
        self.message.setLineWidth(0)
        self.message.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.message.setMargin(0)

        self.verticalLayout.addWidget(self.message, 0, Qt.AlignHCenter)

        self.vertical_spacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.vertical_spacer_2)


        self.retranslateUi(ShutdownOverlay)

        QMetaObject.connectSlotsByName(ShutdownOverlay)
    # setupUi

    def retranslateUi(self, ShutdownOverlay):
        ShutdownOverlay.setWindowTitle(QCoreApplication.translate("ShutdownOverlay", u"Form", None))
        self.message.setText(QCoreApplication.translate("ShutdownOverlay", u"Exiting...", None))
    # retranslateUi

