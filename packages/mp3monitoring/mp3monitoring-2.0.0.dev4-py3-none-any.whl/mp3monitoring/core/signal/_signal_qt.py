from PySide2.QtCore import QObject
from PySide2.QtCore import Signal as QSignal

from mp3monitoring.core.signal._signal_no_qt import Signal as SignalNQ


class Signal(SignalNQ, QObject):
    """
    Use those weird name because of https://bugreports.qt.io/browse/PYSIDE-1264.
    """
    _s: QSignal = QSignal(int)

    def __init__(self):
        super().__init__()

    def s_connect(self, callback):
        self._s.connect(callback)

    def s_disconnect(self):
        try:
            self._s.disconnect()
        except Exception:
            pass

    def s_emit(self, idx: int):
        self._s.emit(idx)
