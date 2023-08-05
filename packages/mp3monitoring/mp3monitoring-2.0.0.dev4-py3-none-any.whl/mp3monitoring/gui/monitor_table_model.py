from PySide2.QtCore import QAbstractTableModel, Qt, QSize, QRect
from PySide2.QtGui import QIcon, QBrush
from PySide2.QtWidgets import QStyledItemDelegate, QStyle

from mp3monitoring.core.manager import Manager
from mp3monitoring.gui import pkg_data


class IconDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._cur_symbol = str(pkg_data.STOPPED_SYMBOL)

    def paint(self, painter, option, index):
        str_to_symbol = {
            "error": pkg_data.ERROR_SYMBOL,
            "ok": pkg_data.OK_SYMBOL,
            "search": pkg_data.SEARCH_SYMBOL,
            "stopped": pkg_data.STOPPED_SYMBOL,
            "wait": pkg_data.WAIT_SYMBOL,
            "stopping": pkg_data.WAIT_SYMBOL,
        }

        if int(option.state) & QStyle.State_Enabled and int(option.state) & QStyle.State_Selected and int(option.state) & QStyle.State_Active:
            brush = QBrush(option.palette.color(option.palette.Highlight))
        elif int(option.state) & QStyle.State_Enabled and int(option.state) & QStyle.State_Selected:
            brush = QBrush(option.palette.color(option.palette.Background))
        else:  # int(option.state) == QStyle.State_Enabled
            brush = QBrush(option.palette.color(option.palette.Base))
        painter.fillRect(option.rect, brush)

        size = min(option.rect.width(), option.rect.height()) * 0.85
        left = (option.rect.width() - size) / 2
        top = option.rect.getCoords()[1] + (option.rect.height() - size) / 2
        pixmap = QIcon(str(str_to_symbol[index.data(Qt.DisplayRole)])).pixmap(QSize(size, size))
        painter.drawPixmap(QRect(left, top, size, size), pixmap)


class DataTableModel(QAbstractTableModel):
    def __init__(self, manager: Manager, parent=None):
        super().__init__(parent)
        self.header_data = ['status', 'source', 'target', 'recursive', 'startup', 'interval (s)']
        self.__manager = manager
        for job in self.__manager.jobs:
            job.status_changed.s_connect(lambda: self.dataChanged.emit(self.index(0, 0), self.index(0, len(self.__manager))))

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.__manager)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.header_data)

    def flags(self, index):
        if not index.isValid() or len(self.__manager) <= 0:
            return Qt.NoItemFlags
        if index.column() == 3 or index.column() == 4 or index.column() == 5:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, col, orientation, role=None):
        """
        Header data is bold and centered.
        :param col:
        :param orientation:
        :param role:
        :return:
        """
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.header_data[col]
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
            elif role == Qt.FontRole:
                font = self.parent().font()
                font.setBold(True)
                font.setPointSize(self.parent().font().pointSize() + 1)
                return font
        return None

    def data(self, index, role=None):
        if not index.isValid() or len(self.__manager) <= 0:
            return None
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.DisplayRole or role == Qt.EditRole or role == Qt.ToolTipRole:
            job = self.__manager.jobs[index.row()]
            if index.column() == 1:
                return str(job.config.source_dir)
            if index.column() == 2:
                return str(job.config.target_dir)
            if index.column() == 3:
                return job.config.recursive
            if index.column() == 4:
                return job.config.run_at_startup
            if index.column() == 5:
                return job.config.sleep_time
        if index.column() == 0:
            job = self.__manager.jobs[index.row()]
            if role == Qt.DisplayRole:
                return job.status
            if role == Qt.ToolTipRole:
                return job.tooltip()
        return None

    def setData(self, index, data, role=None):
        if not index.isValid() or len(self.__manager) <= 0:
            return Qt.NoItemFlags
        if role == Qt.EditRole:
            if index.column() == 4 and isinstance(data, bool):  # run at startup
                job = self.__manager.jobs[index.row()]
                job.config.run_at_startup = data
                self.dataChanged.emit(index, index)
                return True
            if index.column() == 5 and isinstance(data, int):  # sleep time
                job = self.__manager.jobs[index.row()]
                job.config.sleep_time = data
                self.dataChanged.emit(index, index)
                return True
        return False

    def sort(self, p_int, order=None):
        pass
