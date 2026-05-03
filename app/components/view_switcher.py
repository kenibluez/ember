from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QButtonGroup
from PySide6.QtCore import Signal

class ViewSwitcher(QWidget):
    view_changed = Signal(str)

    def __init__(self, modes: list[str]) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        self.group = QButtonGroup(self)

        for mode in modes:
            btn = QPushButton(mode.capitalize())
            btn.setCheckable(True)
            self.group.addButton(btn)
            layout.addWidget(btn)
            btn.clicked.connect(lambda _, m=mode: self.view_changed.emit(m))
