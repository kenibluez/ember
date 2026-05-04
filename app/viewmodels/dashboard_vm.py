from PySide6.QtCore import Signal

from app.services.dashboard_service import DashboardService
from app.viewmodels.base_vm import BaseViewModel


class DashboardViewModel(BaseViewModel):
    stats_updated = Signal(dict)

    def __init__(self, service: DashboardService, parent=None) -> None:
        super().__init__(parent)
        self._service = service

    def load_stats(self) -> None:
        self.loading_changed.emit(True)
        stats = self._service.get_stats()
        self.stats_updated.emit(stats)
        self.loading_changed.emit(False)
