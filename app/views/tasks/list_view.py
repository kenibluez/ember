from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem

class TaskListView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

    def update_tasks(self, tasks: list) -> None:
        self.list_widget.clear()
        for task in tasks:
            item = QListWidgetItem(f"{task.title} - [{task.status}]")
            self.list_widget.addItem(item)
