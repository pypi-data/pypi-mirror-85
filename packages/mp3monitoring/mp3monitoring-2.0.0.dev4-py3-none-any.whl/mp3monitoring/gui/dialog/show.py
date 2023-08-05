from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMessageBox

from mp3monitoring.gui import pkg_data
from mp3monitoring.gui.dialog.about import AboutDialog
from mp3monitoring.gui.dialog.settings import SettingsDialog


def about_dialog(parent=None):
    dialog = AboutDialog(parent)
    dialog.setAttribute(Qt.WA_DeleteOnClose, True)
    dialog.open()


def settings_dialog(settings, manager, parent=None):
    dialog = SettingsDialog(settings, manager, parent)
    dialog.setWindowIcon(QIcon(str(pkg_data.SETTINGS_SYMBOL)))
    dialog.setAttribute(Qt.WA_DeleteOnClose, True)
    dialog.open()


def question_dialog(win_title, msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowIcon(QIcon(str(pkg_data.LOGO_ICON)))

    msg_box.setText(msg)
    msg_box.setWindowTitle(win_title)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    reply = msg_box.exec()
    return reply


def information_dialog(win_title, msg):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowIcon(QIcon(str(pkg_data.LOGO_ICON)))

    msg_box.setText(msg)
    msg_box.setWindowTitle(win_title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()
