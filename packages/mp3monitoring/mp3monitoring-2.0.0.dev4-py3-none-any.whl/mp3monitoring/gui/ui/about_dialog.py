# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.setWindowModality(Qt.WindowModal)
        AboutDialog.resize(567, 315)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Noto Sans")
        AboutDialog.setFont(font)
        self.gridLayout = QGridLayout(AboutDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.top = QWidget(AboutDialog)
        self.top.setObjectName(u"top")
        self.horizontalLayout = QHBoxLayout(self.top)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.logo = QLabel(self.top)
        self.logo.setObjectName(u"logo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setBaseSize(QSize(250, 250))
        self.logo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.logo)

        self.horizontal_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontal_spacer)

        self.right = QWidget(self.top)
        self.right.setObjectName(u"right")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.right.sizePolicy().hasHeightForWidth())
        self.right.setSizePolicy(sizePolicy2)
        self.verticalLayout = QVBoxLayout(self.right)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.name = QLabel(self.right)
        self.name.setObjectName(u"name")
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamily(u"Noto Sans")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.name.setFont(font1)
        self.name.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.name)

        self.vertical_spacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.vertical_spacer_2)

        self.info_widget = QWidget(self.right)
        self.info_widget.setObjectName(u"info_widget")
        self.info_widget.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.info_widget.sizePolicy().hasHeightForWidth())
        self.info_widget.setSizePolicy(sizePolicy3)
        self.info_widget.setFont(font)
        self.gridLayout_7 = QGridLayout(self.info_widget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(9)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.author = QLabel(self.info_widget)
        self.author.setObjectName(u"author")
        self.author.setFont(font)
        self.author.setOpenExternalLinks(True)

        self.gridLayout_7.addWidget(self.author, 1, 2, 1, 1)

        self.license = QLabel(self.info_widget)
        self.license.setObjectName(u"license")
        self.license.setFont(font)
        self.license.setOpenExternalLinks(True)

        self.gridLayout_7.addWidget(self.license, 2, 2, 2, 1)

        self.author_l = QLabel(self.info_widget)
        self.author_l.setObjectName(u"author_l")
        font2 = QFont()
        font2.setFamily(u"Noto Sans")
        font2.setBold(True)
        font2.setWeight(75)
        self.author_l.setFont(font2)

        self.gridLayout_7.addWidget(self.author_l, 1, 0, 1, 1)

        self.license_l = QLabel(self.info_widget)
        self.license_l.setObjectName(u"license_l")
        self.license_l.setFont(font2)

        self.gridLayout_7.addWidget(self.license_l, 2, 0, 2, 1)

        self.version_l = QLabel(self.info_widget)
        self.version_l.setObjectName(u"version_l")
        self.version_l.setFont(font2)

        self.gridLayout_7.addWidget(self.version_l, 0, 0, 1, 1)

        self.version = QLabel(self.info_widget)
        self.version.setObjectName(u"version")
        self.version.setFont(font)

        self.gridLayout_7.addWidget(self.version, 0, 2, 1, 1)

        self.website_l = QLabel(self.info_widget)
        self.website_l.setObjectName(u"website_l")
        self.website_l.setFont(font2)

        self.gridLayout_7.addWidget(self.website_l, 4, 0, 1, 1)

        self.website = QLabel(self.info_widget)
        self.website.setObjectName(u"website")
        self.website.setFont(font)
        self.website.setOpenExternalLinks(True)

        self.gridLayout_7.addWidget(self.website, 4, 2, 1, 1)


        self.verticalLayout.addWidget(self.info_widget)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.vertical_spacer)

        self.update_check = QHBoxLayout()
        self.update_check.setSpacing(7)
        self.update_check.setObjectName(u"update_check")
        self.update_status = QLabel(self.right)
        self.update_status.setObjectName(u"update_status")

        self.update_check.addWidget(self.update_status)

        self.update_info = QLabel(self.right)
        self.update_info.setObjectName(u"update_info")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.update_info.sizePolicy().hasHeightForWidth())
        self.update_info.setSizePolicy(sizePolicy4)
        self.update_info.setFont(font)

        self.update_check.addWidget(self.update_info)


        self.verticalLayout.addLayout(self.update_check)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.right)


        self.gridLayout.addWidget(self.top, 1, 0, 1, 1)


        self.retranslateUi(AboutDialog)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About", None))
        self.name.setText(QCoreApplication.translate("AboutDialog", u"MP3 Monitoring", None))
        self.author.setText(QCoreApplication.translate("AboutDialog", u"<author>", None))
        self.license.setText(QCoreApplication.translate("AboutDialog", u"<license>", None))
        self.author_l.setText(QCoreApplication.translate("AboutDialog", u"Author", None))
        self.license_l.setText(QCoreApplication.translate("AboutDialog", u"License", None))
        self.version_l.setText(QCoreApplication.translate("AboutDialog", u"Version", None))
        self.version.setText(QCoreApplication.translate("AboutDialog", u"<version>", None))
        self.website_l.setText(QCoreApplication.translate("AboutDialog", u"Website", None))
        self.website.setText(QCoreApplication.translate("AboutDialog", u"<website>", None))
        self.update_status.setText("")
        self.update_info.setText(QCoreApplication.translate("AboutDialog", u"Checking for updates...", None))
    # retranslateUi

