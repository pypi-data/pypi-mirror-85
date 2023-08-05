import platform
from pathlib import Path

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog

from mp3monitoring.core.manager import Manager
from mp3monitoring.core.settings import Settings, save_config
from mp3monitoring.gui.dialog import show
from mp3monitoring.gui.ui.settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, settings: Settings, manager: Manager, parent):
        super().__init__(parent)

        self._manager: Manager = manager
        self._settings: Settings = settings

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~(Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint))

        self.start_minimized.setChecked(self._settings.start_minimized)
        self.start_with_system.setChecked(self._settings.start_with_system)

        if platform.system() != "Windows":
            self.start_with_system.hide()
            self.start_with_system_l.hide()

        self.button_box.accepted.connect(self.apply)
        self.button_box.rejected.connect(self.cancel)

    def apply(self):
        settings_changed = False

        if platform.system() == "Windows" and self._settings.start_with_system != self.start_with_system.isChecked():
            startup_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            startup_file = startup_dir.joinpath("MP3 Monitoring GUI.bat")
            if self.start_with_system.isChecked():
                if not startup_dir.is_dir():
                    show.information_dialog("Settings change failed", "Could not find startup directory.\nPlease report this error.")
                else:
                    try:
                        with startup_file.open(mode='w', encoding='utf-8') as writer:
                            writer.writelines(["@echo off\n", "mp3monitoring-gui"])
                    except PermissionError:
                        show.information_dialog("Settings change failed", "Could not create startup item.")
                    else:
                        self._settings.start_with_system = True
                        settings_changed = True
            else:
                try:
                    startup_file.unlink()
                except FileNotFoundError:
                    self._settings.start_with_system = False
                    settings_changed = True
                except PermissionError:
                    show.information_dialog("Settings change failed", "Could not find startup directory.\nPlease report this error.")
                else:
                    self._settings.start_with_system = False
                    settings_changed = True

        if self._settings.start_minimized != self.start_minimized.isChecked():
            self._settings.start_minimized = self.start_minimized.isChecked()
            settings_changed = True
        if settings_changed:
            save_config(self._settings, self._manager.get_configurations())

        self.close()

    def cancel(self):
        self.close()
