from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import QWidget

from mp3monitoring.gui.ui.shutdown_overlay import Ui_ShutdownOverlay


class ShutdownOverlay(QWidget, Ui_ShutdownOverlay):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.fill_color = QColor(30, 30, 30, 120)
        self.text_color = QColor(255, 255, 255, 255)
        self.message.setStyleSheet('color: white')

    def paintEvent(self, event):
        size = self.size()

        # draw background
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(255, 255, 255, 255))
        painter.setBrush(self.fill_color)
        painter.drawRect(0, 0, size.width(), size.height())
        painter.end()
