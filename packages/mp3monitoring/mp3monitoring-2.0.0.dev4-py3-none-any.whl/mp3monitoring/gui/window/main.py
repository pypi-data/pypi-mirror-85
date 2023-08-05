from functools import partial

from PySide2.QtCore import QEvent, Qt, QSize, QItemSelection, QModelIndex
from PySide2.QtGui import QIcon, QCloseEvent
from PySide2.QtWidgets import QHeaderView, QMainWindow, QMenu, QSystemTrayIcon, QApplication, QDialog

from mp3monitoring.core.job import Job
from mp3monitoring.core.manager import Manager
from mp3monitoring.core.settings import save_config, Settings
from mp3monitoring.gui import pkg_data
from mp3monitoring.gui.dialog import show
from mp3monitoring.gui.dialog.add_job import AddJobDialog
from mp3monitoring.gui.monitor_table_model import DataTableModel, IconDelegate
from mp3monitoring.gui.stop_thread import StopThread
from mp3monitoring.gui.ui.main import Ui_MainWindow
from mp3monitoring.gui.widget.shutdown_overlay import ShutdownOverlay


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app: QApplication, settings: Settings, manager: Manager):
        super().__init__()
        self.setupUi(self)

        self._app: QApplication = app
        self._settings: Settings = settings
        self._manager: Manager = manager

        self.setWindowIcon(QIcon(str(pkg_data.LOGO_ICON)))
        self.tray_icon: QSystemTrayIcon = self.create_tray_icon()

        self.overlay: ShutdownOverlay = ShutdownOverlay(self)
        self.gridLayout.addWidget(self.overlay, 0, 0, 1, 1)
        self.overlay.hide()

        self.setup_action_handles()
        self.setup_tool_bar()

        self.create_monitor_table(manager)

        self._stop_thread = StopThread(manager)
        self._stop_thread.finished.connect(self._app.exit)

        if self._settings.start_minimized:
            self.hide()
            self.tray_icon.show()
        else:
            self.show()

    def setup_action_handles(self):
        self.action_about.triggered.connect(partial(show.about_dialog, self))
        self.action_exit.triggered.connect(self.exit)
        self.action_settings.triggered.connect(partial(show.settings_dialog, self._settings, self._manager, self))

        self.action_add_job.triggered.connect(self.handle_add_job)
        self.action_remove_job.triggered.connect(self.handle_remove_job)
        self.action_start_job.triggered.connect(self.handle_start_job)
        self.action_stop_job.triggered.connect(self.handle_stop_job)

        self.action_about.setIcon(QIcon(str(pkg_data.INFO_SYMBOL)))
        self.action_settings.setIcon(QIcon(str(pkg_data.SETTINGS_SYMBOL)))
        self.action_add_job.setIcon(QIcon(str(pkg_data.ADD_SYMBOL)))
        self.action_exit.setIcon(QIcon(str(pkg_data.POWER_SYMBOL)))
        self.action_remove_job.setIcon(QIcon(str(pkg_data.REMOVE_SYMBOL)))
        self.action_start_job.setIcon(QIcon(str(pkg_data.START_SYMBOL)))
        self.action_stop_job.setIcon(QIcon(str(pkg_data.STOP_SYMBOL)))

    def setup_tool_bar(self):
        # disable context menu for the toolbar
        self.tool_bar.toggleViewAction().setEnabled(False)
        icon_size = self.tool_bar.height()
        self.tool_bar.setIconSize(QSize(icon_size, icon_size))

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if int(self.windowState()) & Qt.WindowMinimized:
                self.hide()
                self.tray_icon.show()
                if QSystemTrayIcon.supportsMessages():
                    self.tray_icon.showMessage("MP3 Monitoring is running in background!", "Double click the tray icon to open and right click for menu.")

    def closeEvent(self, event: QCloseEvent, close_immediately=False):
        event.ignore()
        self.exit()

    def exit(self):
        self.menu_bar.setEnabled(False)
        self.tool_bar.setEnabled(False)
        self.overlay.show()
        self.show_window()

        if not self._settings.ignore_config:
            save_config(self._settings, self._manager.get_configurations())
        self._stop_thread.start()

    def create_tray_icon(self):
        tray_icon = QSystemTrayIcon(QIcon(str(pkg_data.LOGO_ICON)))
        tray_icon.activated.connect(self.tray_icon_clicked)

        menu = QMenu(self)
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.show_window)
        menu.addSeparator()
        menu.addAction(self.action_exit)

        tray_icon.setContextMenu(menu)
        return tray_icon

    def tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
        elif reason == QSystemTrayIcon.Context:
            pass  # context menu automatically shown by the system tray icon

    def show_window(self):
        self.tray_icon.hide()
        self.showNormal()
        self.activateWindow()

    def update_job_actions(self, sel_job_idx: int = -1):
        if sel_job_idx > len(self._manager) or sel_job_idx < 0:  # job does not exist
            for action in [self.action_remove_job, self.action_start_job, self.action_stop_job]:
                action.setEnabled(False)
            return
        sel_job = self._manager.jobs[sel_job_idx]
        self.action_remove_job.setEnabled(not sel_job.is_active())
        self.action_start_job.setEnabled(not sel_job.is_active())
        self.action_stop_job.setEnabled(sel_job.is_active() and not sel_job.is_stopping())

    def monitor_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        self.update_job_actions(selected.indexes()[0].row())

    def monitor_data_changed(self, top_left: QModelIndex, bottom_right: QModelIndex, roles):
        sel_idx = self.monitor_table_view.selectedIndexes()
        if len(sel_idx) > 0:
            self.update_job_actions(sel_idx[0].row())
        else:
            self.update_job_actions()

    def create_monitor_table(self, manager: Manager):
        table_model = DataTableModel(manager, self)
        self.monitor_table_view.setModel(table_model)
        self.monitor_table_view.setSortingEnabled(False)

        self.monitor_table_view.setItemDelegateForColumn(0, IconDelegate(self.monitor_table_view))

        h_header = self.monitor_table_view.horizontalHeader()
        h_header.setSectionResizeMode(0, QHeaderView.Fixed)  # status
        h_header.setSectionResizeMode(1, QHeaderView.Stretch)  # source dir
        h_header.setSectionResizeMode(2, QHeaderView.Stretch)  # target dir
        self.monitor_table_view.resizeColumnsToContents()

        table_model.dataChanged.connect(self.monitor_data_changed)
        self.monitor_table_view.selectionModel().selectionChanged.connect(self.monitor_selection_changed)

    def handle_add_job(self):
        """
        Can load ONLY offline profiles at the moment.
        :return:
        """
        dialog = AddJobDialog(self)
        state = dialog.exec()
        if state == QDialog.Accepted:
            config, start = dialog.get_config()
            job = Job(config)
            self._manager.add(job)
            if start:
                job.start()
            self.monitor_table_view.model().modelReset.emit()

    def handle_remove_job(self):
        del self._manager.jobs[self.monitor_table_view.selectionModel().currentIndex().row()]
        self.monitor_table_view.model().modelReset.emit()
        self.update_job_actions()

    def handle_start_job(self):
        self._manager.jobs[self.monitor_table_view.selectionModel().currentIndex().row()].start()

    def handle_stop_job(self):
        self._manager.jobs[self.monitor_table_view.selectionModel().currentIndex().row()].stop(False)

    def handle_check_update(self):
        show.information_dialog('Not implemented yet.', 'Checking for updates is not implemented yet.')
