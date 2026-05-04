from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStyle, QStyleOption
from PySide6.QtGui import QPainter
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

    def paintEvent(self, event) -> None:
        """Required for QSS background-color/border to work on custom QWidget subclasses."""
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)

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

        status_map = {
            "todo": "badge-todo",
            "in_progress": "badge-in_progress",
            "completed": "badge-completed",
            "cancelled": "badge-cancelled",
        }

        self.status_lbl = QLabel(self.task.status.upper())
        self.status_lbl.setObjectName(status_map.get(self.task.status.lower(), "badge-todo"))
        self.status_lbl.setFixedHeight(20)

        self.priority_lbl = QLabel(self.task.priority.upper())
        self.priority_lbl.setObjectName("badge-outline")
        self.priority_lbl.setFixedHeight(20)

        footer.addWidget(self.status_lbl)
        footer.addWidget(self.priority_lbl)
        footer.addStretch()

        layout.addWidget(self.title_lbl)
        layout.addWidget(self.desc_lbl)
        layout.addStretch()
        layout.addLayout(footer)