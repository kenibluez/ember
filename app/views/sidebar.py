from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QButtonGroup, QLabel, QPushButton, QVBoxLayout, QWidget


class Sidebar(QWidget):
    nav_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("sidebar")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)

        logo = QLabel("🔥 EMBER")
        logo.setObjectName("sidebar-logo")
        layout.addWidget(logo)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        nav_items = [
            ("Dashboard", "dashboard"),
            ("Tasks", "tasks"),
            ("Calendar", "calendar"),
            ("Settings", "settings"),
        ]

        for txt, key in nav_items:
            btn = QPushButton(txt)
            btn.setObjectName("nav-btn")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("key", key)

            if key == "dashboard":
                btn.setChecked(True)

            self.group.addButton(btn)
            layout.addWidget(btn)
            btn.clicked.connect(lambda _, k=key: self.nav_changed.emit(k))

        layout.addStretch()
