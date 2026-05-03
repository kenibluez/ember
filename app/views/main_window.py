from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QLabel
)
from PySide6.QtCore import Qt
from app.views.sidebar import Sidebar
from app.core.database import SessionLocal
from app.services.task_service import TaskService
from app.viewmodels.task_vm import TaskViewModel
from app.views.tasks.task_view import TasksView

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

        self.session = SessionLocal()
        self.task_service = TaskService(self.session)
        self.task_vm = TaskViewModel(self.task_service)

    def _navigate(self, key: str) -> None:
        if key not in self._view_cache:
            # Lazy load views on demand
            self._view_cache[key] = self._build_view(key)
            self.stack.addWidget(self._view_cache[key])
        self.stack.setCurrentWidget(self._view_cache[key])
    
    def _build_view(self, key: str) -> QWidget:
        # Placeholder views for now
        match key:
            case "dashboard":
                return QLabel("Dashboard View (Coming Soon)", alignment=Qt.AlignCenter)
            case "tasks":
                return TasksView(self.task_vm)
            case "calendar":
                return QLabel("Calendar View (Coming Soon)", alignment=Qt.AlignCenter)
            case "settings":
                return QLabel("Settings View (Coming Soon)", alignment=Qt.AlignCenter)
            case _:
                return QLabel("Unknown View", alignment=Qt.AlignCenter)