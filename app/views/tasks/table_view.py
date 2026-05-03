from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

class TaskTableModel(QAbstractTableModel):
    def __init__(self, tasks=None) -> None:
        super().__init__()
        self._tasks = tasks or []
        self._headers = ["Status", "Title", "Priority", "Due Date"]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._tasks)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        
        task = self._tasks[index.row()]
        col = index.column()
        
        if col == 0: return task.status.upper()
        if col == 1: return task.title
        if col == 2: return task.priority.upper()
        if col == 3: return task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "-"
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

class TaskTableView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.table = QTableView()
        self.model = TaskTableModel()
        self.table.setModel(self.model)

        # Visual Polish
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        layout.addWidget(self.table)

    def update_tasks(self, tasks: list) -> None:
        self.model.beginResetModel()
        self.model._tasks = tasks
        self.model.endResetModel()
