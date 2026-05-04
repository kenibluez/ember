from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHBoxLayout, QLabel, QStyle, QStyleOption, QVBoxLayout, QWidget, QFrame

from app.styles.theme import Colors


class DayCell(QWidget):
    """A custom widget representing a single day in the grid."""

    def __init__(self, day_number: int, parent=None) -> None:
        super().__init__(parent)
        self.day_number = day_number
        self.events: list = []
        self.setObjectName("day-cell")
        self.setMinimumWidth(100)
        self.setMinimumHeight(150) # Increased for better multi-line support

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(10, 10, 10, 10)
        self.lay.setSpacing(8)
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

        dot = QFrame()
        dot.setObjectName("dot")
        dot.setFixedSize(8, 8)
        # Fallback inline style to ensure visibility
        dot.setStyleSheet(f"background-color: {Colors.EMBER}; border-radius: 4px;")
        layout.addWidget(dot)

        title_label = QLabel(title)
        title_label.setObjectName("event-title")
        title_label.setWordWrap(True)
        layout.addWidget(title_label, stretch=1)

        self.lay.addWidget(container)

    def paintEvent(self, event) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
