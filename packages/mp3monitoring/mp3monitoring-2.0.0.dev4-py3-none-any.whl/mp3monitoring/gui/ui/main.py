# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1197, 324)
        font = QFont()
        font.setFamily(u"Noto Sans")
        MainWindow.setFont(font)
        MainWindow.setWindowTitle(u"MP3 Monitoring")
        MainWindow.setIconSize(QSize(512, 512))
        self.action_add_job = QAction(MainWindow)
        self.action_add_job.setObjectName(u"action_add_job")
        self.action_add_job.setFont(font)
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_exit.setFont(font)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about.setFont(font)
        self.action_remove_job = QAction(MainWindow)
        self.action_remove_job.setObjectName(u"action_remove_job")
        self.action_remove_job.setEnabled(False)
        self.action_remove_job.setFont(font)
        self.action_start_job = QAction(MainWindow)
        self.action_start_job.setObjectName(u"action_start_job")
        self.action_start_job.setEnabled(False)
        self.action_start_job.setFont(font)
        self.action_stop_job = QAction(MainWindow)
        self.action_stop_job.setObjectName(u"action_stop_job")
        self.action_stop_job.setEnabled(False)
        self.action_stop_job.setFont(font)
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.action_settings.setFont(font)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setCursor(QCursor(Qt.ArrowCursor))
        self.central_widget.setAutoFillBackground(False)
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.monitor_table_view = QTableView(self.central_widget)
        self.monitor_table_view.setObjectName(u"monitor_table_view")
        self.monitor_table_view.setFont(font)
        self.monitor_table_view.setFocusPolicy(Qt.ClickFocus)
        self.monitor_table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.monitor_table_view.setFrameShape(QFrame.StyledPanel)
        self.monitor_table_view.setLineWidth(1)
        self.monitor_table_view.setMidLineWidth(0)
        self.monitor_table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.monitor_table_view.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.monitor_table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.monitor_table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.monitor_table_view.setGridStyle(Qt.SolidLine)
        self.monitor_table_view.setSortingEnabled(True)
        self.monitor_table_view.horizontalHeader().setCascadingSectionResizes(False)
        self.monitor_table_view.horizontalHeader().setHighlightSections(False)
        self.monitor_table_view.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.monitor_table_view, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.central_widget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1197, 26))
        self.menu_bar.setFont(font)
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_file.setFont(font)
        self.menu_help = QMenu(self.menu_bar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_help.setFont(font)
        MainWindow.setMenuBar(self.menu_bar)
        self.tool_bar = QToolBar(MainWindow)
        self.tool_bar.setObjectName(u"tool_bar")
        self.tool_bar.setEnabled(True)
        self.tool_bar.setMovable(False)
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.tool_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_add_job)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_settings)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_help.addAction(self.action_about)
        self.tool_bar.addAction(self.action_add_job)
        self.tool_bar.addAction(self.action_remove_job)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.action_start_job)
        self.tool_bar.addAction(self.action_stop_job)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.action_add_job.setText(QCoreApplication.translate("MainWindow", u"Add...", None))
#if QT_CONFIG(tooltip)
        self.action_add_job.setToolTip(QCoreApplication.translate("MainWindow", u"Add a new job", None))
#endif // QT_CONFIG(tooltip)
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"&Exit", None))
#if QT_CONFIG(shortcut)
        self.action_exit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_remove_job.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
#if QT_CONFIG(tooltip)
        self.action_remove_job.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected job", None))
#endif // QT_CONFIG(tooltip)
        self.action_start_job.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(tooltip)
        self.action_start_job.setToolTip(QCoreApplication.translate("MainWindow", u"Start selected job", None))
#endif // QT_CONFIG(tooltip)
        self.action_stop_job.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
#if QT_CONFIG(tooltip)
        self.action_stop_job.setToolTip(QCoreApplication.translate("MainWindow", u"Stop selected job", None))
#endif // QT_CONFIG(tooltip)
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"Settings...", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.tool_bar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        pass
    # retranslateUi

