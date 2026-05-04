from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateTimeEdit,
    QHBoxLayout,
    QPushButton,
    QLabel
)
from app.core.models.task import TaskPriority
from app.core.schemas.task import TaskCreate
from app.styles.theme import Colors
from PySide6.QtCore import QDateTime

class TaskForm(QDialog):
    """Dialog for creating or editing a task."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Task")
        self.setMinimumWidth(400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title
        layout.addWidget(QLabel("TITLE", objectName="form-label"))
        self.title_input = QLineEdit(placeholderText="What needs to be done?")
        layout.addWidget(self.title_input)

        # Description
        layout.addWidget(QLabel("DESCRIPTION", objectName="form-label"))
        self.desc_input = QTextEdit(placeholderText="Add more details...")
        self.desc_input.setMaximumHeight(100)
        layout.addWidget(self.desc_input)

        # Row for Priority and Date
        row = QHBoxLayout()
        
        col1 = QVBoxLayout()
        col1.addWidget(QLabel("PRIORITY", objectName="form-label"))
        self.priority_input = QComboBox()
        self.priority_input.addItems([p.value for p in TaskPriority])
        col1.addWidget(self.priority_input)
        row.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(QLabel("DUE DATE", objectName="form-label"))
        self.date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_input.setCalendarPopup(True)
        col2.addWidget(self.date_input)
        row.addLayout(col2)

        layout.addLayout(row)

        layout.addStretch()

        btns = QHBoxLayout()
        btns.setSpacing(12)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("secondary")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Ignite")
        self.save_btn.setObjectName("primary")
        self.save_btn.clicked.connect(self.accept)
        
        btns.addStretch()
        btns.addWidget(self.cancel_btn)
        btns.addWidget(self.save_btn)

        layout.addLayout(btns)
        
    def get_data(self) -> TaskCreate:
        """Extracts data from form fields and returns a TaskCreate schema."""
        return TaskCreate(
            title=self.title_input.text(),
            description=self.desc_input.toPlainText(),
            priority=TaskPriority(self.priority_input.currentText()),
            due_date=self.date_input.dateTime().toPython(),
        )