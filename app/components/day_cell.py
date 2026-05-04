from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.styles.theme import Colors


class DayCell(QWidget):
    """A custom widget representing a single day in the grid."""

    def __init__(self, day_number: int, parent=None) -> None:
        super().__init__(parent)
        self.day_number = day_number
        self.events: list = []

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(5, 5, 5, 5)
        self.lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.day_label = QLabel(str(day_number) if day_number != 0 else "")
        self.day_label.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {Colors.CINDER}; background-color: {Colors.CHARCOAL};"
        )
        self.lay.addWidget(self.day_label)

        self.setObjectName("day-cell")

    def add_event_dot(self, title: str) -> None:
        """Adds tiny indicator for event"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(5)
        dot = QLabel("")
        dot.setObjectName("dot")
        layout.addWidget(dot)

        title_label = QLabel(title)
        dot.setStyleSheet(f"font-size: 10px; color: {Colors.CINDER};")
        layout.addWidget(title_label)
        container.setLayout(layout)

        self.lay.addWidget(container)
