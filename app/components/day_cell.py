from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QStyle,
    QStyleOption,
    QVBoxLayout,
    QWidget,
)


class DayCell(QWidget):
    """A custom widget representing a single day in the grid."""

    def __init__(self, day_number: int, parent=None) -> None:
        super().__init__(parent)
        self.day_number = day_number
        self.events: list = []
        self.setObjectName("day-cell")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumWidth(100)

        self.setMinimumHeight(180)  # Further increased

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(10, 10, 10, 10)
        self.lay.setSpacing(10)
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

        dot_frame = QFrame()
        dot_frame.setObjectName("dot")
        dot_frame.setFixedSize(8, 8)
        # Explicit style for reliability
        dot_frame.setStyleSheet(
            "background-color: #FF6524; border-radius: 4px; border: none;"
        )
        layout.addWidget(dot_frame)

        title_label = QLabel(title)
        title_label.setObjectName("event-title")
        title_label.setWordWrap(True)
        # Ensure label doesn't clip
        title_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title_label, stretch=1)

        self.lay.addWidget(container)

    def paintEvent(self, event) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
