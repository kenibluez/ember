from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QButtonGroup
)
from PySide6.QtCore import Qt, Signal

class Sidebar(QWidget):
    nav_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("sidebar")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(5)

        logo = QLabel("🔥 Ember")
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
            btn.setObjectName(f"nav-btn")
            btn.setCheckable(True)
            btn.setProperty("key", key)

            if key == "dashboard":
                btn.setChecked(True)

            self.group.addButton(btn)
            layout.addWidget(btn)
            btn.clicked.connect(lambda _, k=key: self.nav_changed.emit(k))

        layout.addStretch()
        self.setLayout(layout)
