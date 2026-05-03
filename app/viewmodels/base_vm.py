from PySide6.QtCore import QObject, Signal

class BaseViewModel(QObject):
    error_occurred  = Signal(str)
    loading_changed = Signal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def _emit_error(self, message: str) -> None:
        self.error_occurred.emit(message)
