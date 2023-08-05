import copy

from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QColor, QPainter, QPen, QBrush
from PySide2.QtWidgets import QWidget


class WaitAnimation(QWidget):
    """
    Based on
    """
    def __init__(self, parent=None, color=QColor(255, 171, 0, 255)):
        super().__init__(parent)

        self._timer = None
        self._time_point = 0

        self.circle_width = 0.3
        self.rotate_length = 5760 / 360 * 42
        self.speed = 12  # 1/16 _degree
        self.color = color

    def radius(self):
        return min(self.width(), self.height()) / 2

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = QPointF(self.width() / 2, self.height() / 2)
        radius = self.radius()
        ellipse_line_width = self.radius() * 60 / 512

        # big ellipse
        pen = QPen()
        pen.setWidth(ellipse_line_width)
        pen.setColor(self.color)
        painter.setPen(pen)
        painter.drawEllipse(center, radius - pen.width() / 2, radius - pen.width() / 2)

        # dots
        pen = QPen()
        pen.setColor(QColor(0, 0, 0, 0))
        painter.setPen(pen)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        dot_size = radius * 200 / 1024
        color = copy.copy(self.color)

        self._change_color(painter, brush, color, 0)
        painter.drawEllipse(QPointF((self.width() - radius - ellipse_line_width / 2) / 2, self.height() / 2), dot_size, dot_size)
        self._change_color(painter, brush, color, 15)
        painter.drawEllipse(center, dot_size, dot_size)
        self._change_color(painter, brush, color, 30)
        painter.drawEllipse(QPointF((self.width() + radius + ellipse_line_width / 2) / 2, self.height() / 2), dot_size, dot_size)

    def _change_color(self, painter, brush, color, alpha_offset):
        color.setAlphaF(self._get_opacity(alpha_offset))
        brush.setColor(color)
        painter.setBrush(brush)

    def showEvent(self, event):
        self._timer = self.startTimer(10)
        self._time_point = 0

    def _get_opacity(self, offset: int):
        one_blink_time = 20
        time = max(self._time_point - offset, 0)
        if time < 0 or time > one_blink_time * 2:
            return 0
        if time <= one_blink_time:
            return time * 1 / one_blink_time
        return 1 - (time - one_blink_time) * 1 / one_blink_time

    def timerEvent(self, event):
        self._time_point = (self._time_point + 1) % 101
        self.update()
