from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton
from app.components.view_switcher import ViewSwitcher
from app.components.task_form import TaskForm
from app.viewmodels.task_vm import TaskViewModel
from app.views.tasks.list_view import TaskListView
from app.views.tasks.table_view import TaskTableView

class TasksView(QWidget):
    """Parent container for all task view modes (List, Table, Cards, Grid)."""

    def __init__(self, vm: TaskViewModel, parent=None) -> None:
        super().__init__(parent)
        self.vm = vm
        self._setup_ui()

        # Connect ViewModel signals to the view stack
        self.vm.tasks_changed.connect(self._on_tasks_updated)
        self.vm.load_tasks()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header: Switcher + Add Button
        header = QHBoxLayout()
        self.switcher = ViewSwitcher(["list", "table", "cards", "grid"])
        self.switcher.view_changed.connect(self._on_mode_switched)

        add_btn = QPushButton("+ Ignite Task")
        add_btn.setObjectName("primary") # Styled in ember.qss
        add_btn.clicked.connect(self._open_task_form)

        header.addWidget(self.switcher)
        header.addStretch()
        header.addWidget(add_btn)

        # View Stack
        self.stack = QStackedWidget()
        self.list_view  = TaskListView()
        self.table_view = TaskTableView()

        self.stack.addWidget(self.list_view)  # Index 0: List
        self.stack.addWidget(self.table_view) # Index 1: Table

        layout.addLayout(header)
        layout.addWidget(self.stack)

    def _on_mode_switched(self, mode: str) -> None:
        mapping = {"list": 0, "table": 1, "cards": 2, "grid": 3}
        self.stack.setCurrentIndex(mapping.get(mode, 0))

    def _on_tasks_updated(self, tasks: list) -> None:
        self.list_view.update_tasks(tasks)
        self.table_view.update_tasks(tasks)

    def _open_task_form(self) -> None:
        form = TaskForm(self)
        if form.exec():
            data = form.get_data()
            self.vm.create_task(data)
