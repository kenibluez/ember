from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QLabel
)
from PySide6.QtCore import Qt
from app.views.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Ember")
        self.setMinimumSize(800, 600)
        self._view_cache: dict[str, QWidget] = {}

        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.stack   = QStackedWidget()

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, stretch=1)
        self.setCentralWidget(root)

        self.sidebar.nav_changed.connect(self._navigate)
        self._navigate("dashboard")

    def _navigate(self, key: str) -> None:
        if key not in self._view_cache:
            # Lazy load views on demand
            self._view_cache[key] = self._build_view(key)
            self.stack.addWidget(self._view_cache[key])
        self.stack.setCurrentWidget(self._view_cache[key])
    
    def _build_view(self, key: str) -> QWidget:
        # Placeholder views for now
        view = QWidget()
        layout = QHBoxLayout(view)
        label = QLabel(f"{key.capitalize()} View Coming Soon!")
        label.setStyleSheet("font-size: 18px; color: #555;")
        layout.addWidget(label, alignment=Qt.AlignCenter)
        return view