from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateTimeEdit,
    QHBoxLayout,
    QPushButton
)
from app.core.models.task import TaskPriority
from app.core.schemas.task import TaskCreate
from PySide6.QtCore import QDateTime

class TaskForm(QDialog):
    """Dialog for creating or editing a task."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Task")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout()

        self.title_input = QLineEdit(placeholderText="Task title")
        self.desc_input = QTextEdit(placeholderText="Task description")

        self.priority_input = QComboBox()
        self.priority_input.addItems([p.value for p in TaskPriority])

        self.date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_input.setCalendarPopup(True)

        btns = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btns.addWidget(self.save_btn)
        btns.addWidget(self.cancel_btn)

        layout.addWidget(self.title_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.priority_input)
        layout.addWidget(self.date_input)
        layout.addLayout(btns)
        self.setLayout(layout)
        
    def get_data(self) -> TaskCreate:
        """Extracts data from form fields and returns a TaskCreate schema."""
        return TaskCreate(
            title=self.title_input.text(),
            description=self.desc_input.toPlainText(),
            priority=TaskPriority(self.priority_input.currentText()),
            due_date=self.date_input.dateTime().toPython(),
        )