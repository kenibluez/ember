from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QScrollArea
from app.styles.theme import Colors

from app.components.view_switcher import ViewSwitcher
from app.viewmodels.calendar_vm import CalendarViewModel
from app.views.calendar.month_view import MonthView


class CalendarView(QWidget):
    def __init__(self, vm: CalendarViewModel, parent=None) -> None:
        super().__init__(parent)
        self.vm = vm
        self._setup_ui()

        self.vm.events_updated.connect(self._on_events_updated)
        self.vm.load_events()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Header
        header_lay = QHBoxLayout()
        header = QLabel("Calendar")
        header.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {Colors.SMOKE};")
        header_lay.addWidget(header)
        header_lay.addStretch()

        # Switcher
        self.switcher = ViewSwitcher(["month", "week", "day", "year"])
        self.switcher.view_changed.connect(self._on_mode_switched)
        header_lay.addWidget(self.switcher)
        
        layout.addLayout(header_lay)

        # Scroll Area for the View Stack
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll.setStyleSheet(f"background-color: {Colors.VOID};")

        # Stack
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background-color: {Colors.VOID};")
        self.month_view = MonthView()

        # Placeholders for the other views
        self.stack.addWidget(self.month_view)
        
        self.scroll.setWidget(self.stack)
        layout.addWidget(self.scroll)

    def _on_mode_switched(self, mode: str) -> None:
        # Extend mapping as other views are added
        mapping = {"month": 0, "week": 1, "day": 2, "year": 3}
        self.stack.setCurrentIndex(mapping.get(mode, 0))

    def _on_events_updated(self, events: list) -> None:
        self.month_view.update_events(events)
