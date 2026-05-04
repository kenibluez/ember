from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from app.core.schemas.task import TaskRead
from app.core.models.task import TaskStatus

class TaskCard(QWidget):
    """A simple card widget to display task information in a compact format."""

    def __init__(self, task: TaskRead, parent=None) -> None:
        super().__init__(parent)
        self.task = task
        self.setObjectName("task-card") 
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.title_lbl = QLabel(self.task.title)
        self.title_lbl.setObjectName("task-title")
        self.title_lbl.setWordWrap(True)

        self.desc_lbl = QLabel(self.task.description or "No description provided.")
        self.desc_lbl.setObjectName("muted-text")
        self.desc_lbl.setWordWrap(True)

        footer = QHBoxLayout()
        
        # Map task status to its corresponding QSS object name
        status_map = {
            TaskStatus.TODO: "badge-todo",
            TaskStatus.IN_PROGRESS: "badge-in_progress",
            TaskStatus.COMPLETED: "badge-completed",
            TaskStatus.CANCELLED: "badge-cancelled"
        }
        
        self.status_lbl = QLabel(self.task.status.upper())
        self.status_lbl.setObjectName(status_map.get(self.task.status, "badge-todo"))

        self.priority_lbl = QLabel(self.task.priority.upper())
        self.priority_lbl.setObjectName("badge-outline")

        footer.addWidget(self.status_lbl)
        footer.addWidget(self.priority_lbl)
        footer.addStretch()

        layout.addWidget(self.title_lbl)
        layout.addWidget(self.desc_lbl)
        layout.addStretch()
        layout.addLayout(footer)

