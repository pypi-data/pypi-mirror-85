from PySide2.QtCore import Qt
from PySide2.QtGui import QPaintEvent
from PySide2.QtWidgets import QStyle, QStyleOptionTab, QTabBar, QStylePainter, QTabWidget


class VerticalTabBar(QTabBar):
    def paintEvent(self, event: QPaintEvent):
        painter = QStylePainter(self)
        option = QStyleOptionTab()
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QStyle.CE_TabBarTabShape, option)
            painter.drawText(self.tabRect(index), Qt.AlignCenter | Qt.TextDontClip, self.tabText(index))

    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        if size.width() < size.height():
            size.transpose()
        return size


class VerticalTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabBar(VerticalTabBar())
