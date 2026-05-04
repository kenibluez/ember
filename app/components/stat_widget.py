from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLabel, QStyle, QStyleOption, QVBoxLayout, QWidget


class StatWidget(QWidget):
    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("stat-card")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True) # Added for extra reliability

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label = QLabel("0")
        self.value_label.setObjectName("stat-value")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(title.upper())
        self.title_label.setObjectName("stat-title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.value_label)
        layout.addWidget(self.title_label)

    def set_value(self, value: int | str) -> None:
        self.value_label.setText(str(value))

    def paintEvent(self, event) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
