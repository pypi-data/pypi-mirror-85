from pathlib import Path

from PySide2.QtCore import QTime, Qt
from PySide2.QtWidgets import QFileDialog, QDialog

from mp3monitoring.core.job import JobConfig
from mp3monitoring.gui.ui.add_job_dialog import Ui_AddJobDialog


class AddJobDialog(QDialog, Ui_AddJobDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.set_item_actions()

        self.start_job: bool = False

        self.update_gui()

    def set_item_actions(self):
        self.source_dialog_button.clicked.connect(self.source_dir_dialog)
        self.target_dialog_button.clicked.connect(self.target_dir_dialog)
        self.cancel_button.clicked.connect(lambda: self.reject())
        self.add_button.clicked.connect(lambda: self.accept())
        self.add_and_start_button.clicked.connect(self.add_start)

        self.source_dir.textChanged.connect(self.update_gui)
        self.target_dir.textChanged.connect(self.update_gui)

    def add_start(self):
        self.start_job = True
        self.accept()

    def source_dir_dialog(self):
        selected_dir = QFileDialog.getExistingDirectory(self.parent(), 'Select a source directory', options=QFileDialog.ShowDirsOnly)
        self.source_dir.setText(selected_dir)

    def target_dir_dialog(self):
        selected_dir = QFileDialog.getExistingDirectory(self.parent(), 'Select a target directory', options=QFileDialog.ShowDirsOnly)
        self.target_dir.setText(selected_dir)

    def get_config(self):
        return JobConfig(Path(self.source_dir.text()), Path(self.target_dir.text()), self.run_at_startup.isChecked(),
                         QTime(0, 0, 0).secsTo(self.sleep_time.time()), self.recursive_search.isChecked()), self.start_job

    def update_gui(self):
        # background-color: #FFCCCB;
        success = True
        if self.source_dir.text() == "":
            self.source_dir.setStyleSheet("background-color: #FFCCCB;")
            success = False
        else:
            self.source_dir.setStyleSheet("")
        if self.target_dir.text() == "":
            self.target_dir.setStyleSheet("background-color: #FFCCCB;")
            success = False
        else:
            self.target_dir.setStyleSheet("")

        self.add_button.setEnabled(success)
        self.add_and_start_button.setEnabled(success)
