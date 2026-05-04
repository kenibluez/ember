from app.viewmodels.dashboard_vm import DashboardViewModel
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from app.components.stat_widget import StatWidget


class DashboardView(QWidget):
    def __init__(self, vm: DashboardViewModel, parent=None) -> None:
        super().__init__(parent)
        self.vm = vm
        self._setup_ui()

        self.vm.stats_updated.connect(self._on_stats_updated)
        self.vm.load_stats()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Header
        header = QLabel("Overview")
        header.setStyleSheet("font-size: 24px; font-weight: 600; color: #F2F2F2;")
        layout.addWidget(header)

        # Stats Grid
        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        self.stat_total = StatWidget("Total Tasks")
        self.stat_todo = StatWidget("To Do")
        self.stat_progress = StatWidget("In Progress")
        self.stat_done = StatWidget("Completed")
        self.stat_due = StatWidget("Due Today")

        self.grid.addWidget(self.stat_total, 0, 0)
        self.grid.addWidget(self.stat_todo, 0, 1)
        self.grid.addWidget(self.stat_progress, 0, 2)
        self.grid.addWidget(self.stat_done, 1, 0)
        self.grid.addWidget(self.stat_due, 1, 1, 1, 2)  # Spans two columns

        layout.addLayout(self.grid)
        layout.addStretch()

    def _on_stats_updated(self, stats: dict) -> None:
        self.stat_total.set_value(stats.get("total", 0))
        self.stat_todo.set_value(stats.get("todo", 0))
        self.stat_progress.set_value(stats.get("in_progress", 0))
        self.stat_done.set_value(stats.get("done", 0))
        self.stat_due.set_value(stats.get("due_today", 0))
