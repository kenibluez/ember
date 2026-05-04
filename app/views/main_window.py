from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QStackedWidget, QWidget

from app.core.database import SessionLocal
from app.services.calendar_service import CalendarService
from app.services.dashboard_service import DashboardService
from app.services.task_service import TaskService
from app.styles.theme import Colors
from app.viewmodels.calendar_vm import CalendarViewModel
from app.viewmodels.dashboard_vm import DashboardViewModel
from app.viewmodels.task_vm import TaskViewModel
from app.views.calendar.calendar_view import CalendarView
from app.views.dashboard.dashboard_view import DashboardView
from app.views.sidebar import Sidebar
from app.views.tasks.task_view import TasksView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Ember")
        self.setMinimumSize(800, 600)
        self._view_cache: dict[str, QWidget] = {}

        self.session = SessionLocal()
        self.task_service = TaskService(self.session)
        self.task_vm = TaskViewModel(self.task_service)
        self.dashboard_service = DashboardService(self.session)
        self.dashboard_vm = DashboardViewModel(self.dashboard_service)
        self.calendar_service = CalendarService(self.session)
        self.calendar_vm = CalendarViewModel(self.calendar_service)

        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.stack = QStackedWidget()
        self.stack.setObjectName("main-stack")
        self.stack.setStyleSheet(f"background-color: {Colors.VOID};")

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
        match key:
            case "dashboard":
                return DashboardView(self.dashboard_vm)
            case "tasks":
                return TasksView(self.task_vm)
            case "calendar":
                return CalendarView(self.calendar_vm)
            case "settings":
                return QLabel(
                    "Settings View (Coming Soon)",
                    alignment=Qt.AlignmentFlag.AlignCenter,
                )
            case _:
                return QLabel("Unknown View", alignment=Qt.AlignmentFlag.AlignCenter)
