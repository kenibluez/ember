from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from app.core.schemas.task import TaskRead

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
        self.status_lbl = QLabel(self.task.status.upper())
        self.status_lbl.setObjectName(f"badge-{self.task.status.value}")

        self.priority_lbl = QLabel(self.task.priority.upper())
        self.priority_lbl.setObjectName(f"badge-outline")

        footer.addWidget(self.status_lbl)
        footer.addWidget(self.priority_lbl)
        footer.addStretch()

        layout.addWidget(self.title_lbl)
        layout.addWidget(self.desc_lbl)
        layout.addStrech()
        layout.addLayout(footer)

