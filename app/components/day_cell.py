from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.styles.theme import Colors


class DayCell(QWidget):
    """A custom widget representing a single day in the grid."""

    def __init__(self, day_number: int, parent=None) -> None:
        super().__init__(parent)
        self.day_number = day_number
        self.events: list = []
        self.setObjectName("day-cell")
        self.setMinimumSize(100, 100)

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(8, 8, 8, 8)
        self.lay.setSpacing(6)
        self.lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.day_label = QLabel(str(day_number) if day_number != 0 else "")
        self.day_label.setObjectName("day-number")
        self.lay.addWidget(self.day_label)

    def add_event_dot(self, title: str) -> None:
        """Adds tiny indicator for event"""
        container = QWidget()
        container.setObjectName("event-container")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        dot = QWidget()
        dot.setObjectName("dot")
        dot.setFixedSize(8, 8)
        layout.addWidget(dot)

        title_label = QLabel(title)
        title_label.setObjectName("event-title")
        title_label.setWordWrap(True)
        # Avoid explicit styling here to allow QSS to take over
        layout.addWidget(title_label, stretch=1)

        self.lay.addWidget(container)
