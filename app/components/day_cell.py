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

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(8, 8, 8, 8)
        self.lay.setSpacing(4)
        self.lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.day_label = QLabel(str(day_number) if day_number != 0 else "")
        self.day_label.setObjectName("day-number")
        self.lay.addWidget(self.day_label)

    def add_event_dot(self, title: str) -> None:
        """Adds tiny indicator for event"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        dot = QLabel("")
        dot.setObjectName("dot")
        dot.setFixedSize(6, 6)
        layout.addWidget(dot)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 11px; color: {Colors.SMOKE};")
        layout.addWidget(title_label)
        layout.addStretch()

        self.lay.addWidget(container)
