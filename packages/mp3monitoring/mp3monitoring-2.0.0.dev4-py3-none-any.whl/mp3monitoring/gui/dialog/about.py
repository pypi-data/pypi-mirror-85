from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog

from mp3monitoring import static_data
from mp3monitoring.gui import pkg_data
from mp3monitoring.gui.ui.about_dialog import Ui_AboutDialog
from mp3monitoring.gui.updater import UpdateCheckThread


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~(Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint))

        # set descriptions
        self.version.setText(static_data.VERSION)
        self.author.setText(f"<a href=\"{static_data.AUTHOR_GITHUB}\">{static_data.AUTHOR}</a>")
        self.license.setText("<a href=\"https://github.com/IceflowRE/mp3monitoring/blob/main/LICENSE.md\">GPLv3</a>")
        self.website.setText(f"<a href=\"{static_data.PROJECT_URL}\">Github</a>")

        # set logo
        self.logo.setPixmap(QIcon(str(pkg_data.LOGO_ICON)).pixmap(QSize(250, 250)))

        self.update_status.setPixmap(QIcon(str(pkg_data.WAIT_SYMBOL)).pixmap(QSize(self.update_info.height() * 0.8, self.update_info.height() * 0.8)))
        self._update_check = UpdateCheckThread()
        self._update_check.finished.connect(self.change_update_check)
        self._update_check.start()

    def change_update_check(self):
        if not self._update_check.check_succeed:
            self.update_status.setPixmap(QIcon(str(pkg_data.ERROR_SYMBOL)).pixmap(QSize(self.update_info.height() * 0.8, self.update_info.height() * 0.8)))
            self.update_info.setText(self._update_check.err_msg)
            return
        if self._update_check.update_available:
            self.update_status.setPixmap(QIcon(str(pkg_data.WARNING_SYMBOL)).pixmap(QSize(self.update_info.height() * 0.8, self.update_info.height() * 0.8)))
            self.update_info.setText("An Update is available.")
        else:
            self.update_status.setPixmap(QIcon(str(pkg_data.OK_SYMBOL)).pixmap(QSize(self.update_info.height() * 0.8, self.update_info.height() * 0.8)))
            self.update_info.setText("MP3 Monitoring is up to date.")
