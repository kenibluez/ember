from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea
from PySide6.QtCore import Qt
from app.components.task_card import TaskCard

class TaskGridView(QWidget):
    """Grid display strategy for tasks."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.columns = 3
        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area Setup
        self.scrollable = QScrollArea()
        self.scrollable.setObjectName("grid-container")
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scrollable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Container for the Grid
        self.container = QWidget()
        self.container.setObjectName("grid-container") 
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.scrollable.setWidget(self.container)
        main_layout.addWidget(self.scrollable)

    def update_tasks(self, tasks: list) -> None:
        # 1. Clear existing cards
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 2. Re-populate grid
        for i, task in enumerate(tasks):
            card = TaskCard(task)
            row = i // self.columns
            col = i % self.columns
            self.grid.addWidget(card, row, col)