from PySide2.QtCore import QThread

from mp3monitoring.core.manager import Manager


class StopThread(QThread):
    def __init__(self, manager: Manager):
        super().__init__()
        self._manager: Manager = manager

    def run(self):
        self._manager.stop(False)
        self._manager.join()
