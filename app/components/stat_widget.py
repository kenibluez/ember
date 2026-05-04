from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.styles.theme import Colors


class StatWidget(QWidget):
    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("stat-card")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label = QLabel("0")
        self.value_label.setStyleSheet(
            f"font-size: 32px; font-weight: bold; color: {Colors.CHARCOAL};"
        )
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(title.upper())
        self.title_label.setStyleSheet(
            f"font-size:32px; font-weight: 600; color: {Colors.CHARCOAL};"
        )
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.value_label)
        layout.addWidget(self.title_label)

    def set_value(self, value: int | str) -> None:
        self.value_label.setText(str(value))
