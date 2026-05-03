# 🔥 Ember — Implementation Plan

> *"Tasks that never quite go out."*  
> Version 1.0 | May 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack & Dependencies](#2-tech-stack--dependencies)
3. [Design System](#3-design-system)
4. [Architecture & Design Patterns](#4-architecture--design-patterns)
5. [Project Structure](#5-project-structure)
6. [Database Layer](#6-database-layer)
7. [Services Layer](#7-services-layer)
8. [ViewModels Layer](#8-viewmodels-layer)
9. [Views & Components](#9-views--components)
10. [Notifications](#10-notifications)
11. [Styling](#11-styling)
12. [Build Order](#12-build-order)
13. [Environment Setup](#13-environment-setup)
14. [Conventions & Rules](#14-conventions--rules)
15. [Testing Strategy](#15-testing-strategy)

---

## 1. Project Overview

**Ember** is a minimalist desktop task manager built with PySide6.  
The name reflects the core metaphor: tasks are embers — smoldering until
finished, then gone to ash. The UI follows this language.

### Features

- ✅ Task manager with 4 view modes: Grid, Cards, List, Table
- 📅 Calendar with Day, Week, Month, and Year views
- 📊 Simple dashboard with stats and summaries
- 🔔 Desktop notifications via system tray
- 💾 Local SQLite database — no internet, no accounts, no nonsense

### Non-Goals (v1.0)

- No cloud sync
- No collaborative features
- No mobile
- No plugin system

---

## 2. Tech Stack & Dependencies

### Runtime Dependencies

```toml
# requirements.txt
PySide6>=6.7.0
SQLAlchemy>=2.0.0
pydantic>=2.0.0
python-dateutil>=2.9.0
alembic>=1.13.0
```

### Dev Dependencies

```toml
# requirements-dev.txt
pytest>=8.0.0
pytest-qt>=4.4.0
black>=24.0.0
mypy>=1.10.0
```

### Why These?

| Package | Reason |
|---|---|
| `PySide6` | Official Qt6 bindings, LGPL licensed |
| `SQLAlchemy` | Clean ORM, great query API, future-proof |
| `pydantic v2` | Fast validation, free serialization, great DX |
| `python-dateutil` | Sane date manipulation (stdlib calendar is painful) |
| `alembic` | DB migrations — you will change the schema, trust the plan |
| `pytest-qt` | Qt-aware testing, handles the event loop for you |

### Python Version

Minimum: **Python 3.11**  
Reason: `tomllib` stdlib, better type hints, `StrEnum` support.

---

## 3. Design System

### Brand

- **Name:** Ember
- **Tagline:** *"Stop smoldering. Start finishing."*
- **Tone:** Minimalist, slightly sarcastic, dark UI

### Color Palette

```python
# app/styles/theme.py

class Colors:
    # Backgrounds
    VOID      = "#111111"   # Main background
    CHARCOAL  = "#1C1C1C"   # Surface (cards, panels)
    ASH       = "#2B2B2B"   # Components (inputs, rows)

    # Brand
    EMBER     = "#FF6524"   # Primary — orange
    BURN      = "#E8311A"   # Secondary — red

    # Text
    SMOKE     = "#F2F2F2"   # Primary text
    CINDER    = "#888888"   # Muted/secondary text

    # Status (semantic)
    TODO        = "#888888"   # Not started
    IN_PROGRESS = "#FF6524"   # In progress
    CANCELLED   = "#E8311A"   # Cancelled
    DONE        = "#3A3A3A"   # Completed (dimmed intentionally)
```

### Typography

- **UI Font:** `Inter` (bundle with app) — fallback `Segoe UI` / `SF Pro`
- **Monospace:** `JetBrains Mono` — for table/code-adjacent content
- **Logo wordmark:** `ember` — all lowercase, letter-spacing: 0.15em

### Font Scale

| Role | Size | Weight |
|---|---|---|
| Heading 1 | 24px | 600 |
| Heading 2 | 18px | 600 |
| Body | 14px | 400 |
| Caption | 12px | 400 |
| Badge | 11px | 500 |

### Task States

```text
○  To Do        →  not started  (#888888)
◑  In Progress  →  in progress  (#FF6524)
●  Done         →  completed    (#3A3A3A)
✕  Cancelled    →  cancelled    (#E8311A)
```

### Icon Style

- Use `Material Symbols` or `Phosphor Icons` — outline weight, consistent size
- No filled icons in the default state — fill only on hover/active
- Size: 20px UI icons, 16px inline icons

---

## 4. Architecture & Design Patterns

### Pattern: MVVM

```text
┌─────────┐    signals/slots    ┌─────────────┐    method calls    ┌─────────┐
│  Views  │ ◄────────────────► │ ViewModels  │ ──────────────────► │ Services│
└─────────┘                    └─────────────┘                     └─────────┘
                                                                         │
                                                                    method calls
                                                                         │
                                                                         ▼
                                                                  ┌────────────┐
                                                                  │Repositories│
                                                                  └────────────┘
                                                                         │
                                                                         ▼
                                                                   ┌──────────┐
                                                                   │  SQLite  │
                                                                   └──────────┘
```

### Design Patterns Reference

| Pattern | Location | Description |
|---|---|---|
| **MVVM** | Global | View ↔ ViewModel via signals, VM calls Services |
| **Repository** | `app/core/repositories/` | All DB queries live here, nowhere else |
| **Facade** | `app/services/` | Clean API over repositories for ViewModels |
| **Singleton** | `app/core/database.py` | One DB session manager, app-wide |
| **Observer** | Qt signals/slots | ViewModels emit, Views listen |
| **Strategy** | `app/views/tasks/` | 4 views, same data, swappable render strategy |
| **Delegate** | `app/components/delegates/` | Custom Qt item rendering per view type |
| **Lazy Init** | `app/views/main_window.py` | Views instantiated only on first navigation |
| **Composite** | All views | QWidget trees, layouts composing layouts |

### Layer Rules (strictly enforced)

```text
✅ View        → can call ViewModel methods
✅ ViewModel   → can call Service methods
✅ Service     → can call Repository methods
✅ Repository  → can use SQLAlchemy Session

❌ View        → NEVER access Repository or DB directly
❌ ViewModel   → NEVER import SQLAlchemy models directly
❌ Service     → NEVER import Qt or PySide6
❌ Repository  → NEVER contain business logic
```

Breaking these rules will cause pain. Respect the layers.

---

## 5. Project Structure

```text
ember/
├── main.py                          # App entry point
├── ember.db                         # SQLite DB (gitignored)
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
│
├── assets/
│   ├── fonts/
│   │   ├── Inter-Regular.ttf
│   │   ├── Inter-SemiBold.ttf
│   │   └── JetBrainsMono-Regular.ttf
│   └── icons/
│       └── ember.ico
│
├── tests/
│   ├── conftest.py
│   ├── test_services/
│   │   ├── test_task_service.py
│   │   └── test_calendar_service.py
│   └── test_viewmodels/
│       └── test_task_vm.py
│
└── app/
    ├── __init__.py
    │
    ├── core/
    │   ├── database.py              # Engine, Session, Base
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── task.py              # SQLAlchemy Task model
    │   │   └── event.py             # SQLAlchemy Event model
    │   ├── repositories/
    │   │   ├── base_repository.py   # Generic CRUD base
    │   │   ├── task_repository.py
    │   │   └── event_repository.py
    │   └── schemas/
    │       ├── task.py              # Pydantic schemas
    │       └── event.py
    │
    ├── services/
    │   ├── task_service.py          # Business logic for tasks
    │   ├── calendar_service.py      # Business logic for events
    │   ├── notification_service.py  # Tray notification scheduler
    │   └── dashboard_service.py     # Aggregated stats
    │
    ├── viewmodels/
    │   ├── base_vm.py               # Base class with common signals
    │   ├── task_vm.py
    │   ├── calendar_vm.py
    │   ├── dashboard_vm.py
    │   └── notification_vm.py
    │
    ├── views/
    │   ├── main_window.py           # Root window + QStackedWidget
    │   ├── sidebar.py               # Navigation sidebar
    │   ├── dashboard/
    │   │   └── dashboard_view.py
    │   ├── tasks/
    │   │   ├── tasks_view.py        # Parent, owns view switcher
    │   │   ├── list_view.py
    │   │   ├── table_view.py
    │   │   ├── card_view.py
    │   │   └── grid_view.py
    │   └── calendar/
    │       ├── calendar_view.py     # Parent, owns view switcher
    │       ├── day_view.py
    │       ├── week_view.py
    │       ├── month_view.py
    │       └── year_view.py
    │
    ├── components/
    │   ├── delegates/
    │   │   ├── card_delegate.py
    │   │   └── grid_delegate.py
    │   ├── ember_button.py          # Styled QPushButton
    │   ├── task_card.py             # Standalone card widget
    │   ├── badge.py                 # Status badge widget
    │   ├── stat_widget.py           # Dashboard stat block
    │   ├── view_switcher.py         # Toggle button group for view modes
    │   └── task_form.py             # Create/edit task dialog
    │
    └── styles/
        ├── theme.py                 # Color/font constants (Python)
        └── ember.qss                # Global Qt stylesheet
```

---

## 6. Database Layer

### 6.1 Setup

```python
# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Generator

DATABASE_URL = "sqlite:///ember.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    from app.core.models import task, event  # noqa: F401
    Base.metadata.create_all(bind=engine)
```

### 6.2 Task Model

```python
# app/core/models/task.py

from sqlalchemy import String, Text, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import StrEnum
from app.core.database import Base


class TaskStatus(StrEnum):
    TODO        = "todo"
    IN_PROGRESS = "in_progress"
    DONE        = "done"
    CANCELLED   = "cancelled"


class TaskPriority(StrEnum):
    LOW    = "low"
    MEDIUM = "medium"
    HIGH   = "high"


class Task(Base):
    __tablename__ = "tasks"

    id:          Mapped[int]           = mapped_column(primary_key=True)
    title:       Mapped[str]           = mapped_column(String(255))
    description: Mapped[str | None]    = mapped_column(Text, nullable=True)
    status:      Mapped[TaskStatus]    = mapped_column(
                                           SAEnum(TaskStatus),
                                           default=TaskStatus.TODO
                                         )
    priority:    Mapped[TaskPriority]  = mapped_column(
                                           SAEnum(TaskPriority),
                                           default=TaskPriority.MEDIUM
                                         )
    due_date:    Mapped[datetime | None] = mapped_column(
                                             DateTime, nullable=True
                                           )
    created_at:  Mapped[datetime]      = mapped_column(
                                           DateTime,
                                           default=datetime.utcnow
                                         )
    updated_at:  Mapped[datetime]      = mapped_column(
                                           DateTime,
                                           default=datetime.utcnow,
                                           onupdate=datetime.utcnow
                                         )
```

### 6.3 Event Model

```python
# app/core/models/event.py

from sqlalchemy import String, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id:          Mapped[int]        = mapped_column(primary_key=True)
    title:       Mapped[str]        = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text,     nullable=True)
    start_dt:    Mapped[datetime]   = mapped_column(DateTime)
    end_dt:      Mapped[datetime]   = mapped_column(DateTime)
    all_day:     Mapped[bool]       = mapped_column(Boolean, default=False)
    created_at:  Mapped[datetime]   = mapped_column(
                                        DateTime, default=datetime.utcnow
                                      )
```

### 6.4 Pydantic Schemas

```python
# app/core/schemas/task.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.core.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title:       str
    description: str | None = None
    status:      TaskStatus = TaskStatus.TODO
    priority:    TaskPriority = TaskPriority.MEDIUM
    due_date:    datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str | None = None  # all fields optional on update


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id:         int
    created_at: datetime
    updated_at: datetime
```

### 6.5 Base Repository

```python
# app/core/repositories/base_repository.py

from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: Type[ModelT], session: Session) -> None:
        self.model = model
        self.session = session

    def get(self, id: int) -> ModelT | None:
        return self.session.get(self.model, id)

    def get_all(self) -> list[ModelT]:
        return self.session.query(self.model).all()

    def create(self, obj: ModelT) -> ModelT:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True
```

### 6.6 Task Repository

```python
# app/core/repositories/task_repository.py

from sqlalchemy.orm import Session
from app.core.repositories.base_repository import BaseRepository
from app.core.models.task import Task, TaskStatus


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: Session) -> None:
        super().__init__(Task, session)

    def get_by_status(self, status: TaskStatus) -> list[Task]:
        return (
            self.session.query(Task)
            .filter(Task.status == status)
            .all()
        )

    def get_due_soon(self, within_minutes: int = 30) -> list[Task]:
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        threshold = now + timedelta(minutes=within_minutes)
        return (
            self.session.query(Task)
            .filter(Task.due_date.between(now, threshold))
            .filter(Task.status != TaskStatus.DONE)
            .all()
        )
```

---

## 7. Services Layer

Services contain all business logic. They use repositories for data access
and emit nothing Qt-related — they are pure Python.

```python
# app/services/task_service.py

from sqlalchemy.orm import Session
from app.core.repositories.task_repository import TaskRepository
from app.core.models.task import Task, TaskStatus
from app.core.schemas.task import TaskCreate, TaskUpdate, TaskRead


class TaskService:
    def __init__(self, session: Session) -> None:
        self.repo = TaskRepository(session)

    def get_all(self) -> list[TaskRead]:
        tasks = self.repo.get_all()
        return [TaskRead.model_validate(t) for t in tasks]

    def create(self, data: TaskCreate) -> TaskRead:
        task = Task(**data.model_dump())
        created = self.repo.create(task)
        return TaskRead.model_validate(created)

    def update(self, id: int, data: TaskUpdate) -> TaskRead | None:
        task = self.repo.get(id)
        if not task:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.repo.session.commit()
        self.repo.session.refresh(task)
        return TaskRead.model_validate(task)

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)

    def mark_as(self, id: int, status: TaskStatus) -> TaskRead | None:
        return self.update(id, TaskUpdate(status=status))  # type: ignore[arg-type]
```

```python
# app/services/dashboard_service.py

from sqlalchemy.orm import Session
from app.core.models.task import TaskStatus
from app.core.repositories.task_repository import TaskRepository
from app.core.repositories.event_repository import EventRepository
from datetime import date


class DashboardService:
    def __init__(self, session: Session) -> None:
        self.task_repo  = TaskRepository(session)
        self.event_repo = EventRepository(session)

    def get_stats(self) -> dict:
        tasks = self.task_repo.get_all()
        return {
            "total":       len(tasks),
            "todo":        sum(1 for t in tasks if t.status == TaskStatus.TODO),
            "in_progress": sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS),
            "done":        sum(1 for t in tasks if t.status == TaskStatus.DONE),
            "cancelled":   sum(1 for t in tasks if t.status == TaskStatus.CANCELLED),
            "due_today":   sum(
                               1 for t in tasks
                               if t.due_date and t.due_date.date() == date.today()
                           ),
        }
```

---

## 8. ViewModels Layer

ViewModels translate service data into something views can consume.
They own Qt signals and hold view state.

```python
# app/viewmodels/base_vm.py

from PySide6.QtCore import QObject, Signal


class BaseViewModel(QObject):
    error_occurred  = Signal(str)
    loading_changed = Signal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def _emit_error(self, message: str) -> None:
        self.error_occurred.emit(message)
```

```python
# app/viewmodels/task_vm.py

from PySide6.QtCore import Signal
from app.viewmodels.base_vm import BaseViewModel
from app.services.task_service import TaskService
from app.core.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.core.models.task import TaskStatus


class TaskViewModel(BaseViewModel):
    tasks_changed = Signal(list)    # emits list[TaskRead]
    task_created  = Signal(object)  # emits TaskRead
    task_deleted  = Signal(int)     # emits task id

    def __init__(self, service: TaskService, parent=None) -> None:
        super().__init__(parent)
        self._service = service
        self._tasks: list[TaskRead] = []

    def load_tasks(self) -> None:
        self.loading_changed.emit(True)
        self._tasks = self._service.get_all()
        self.tasks_changed.emit(self._tasks)
        self.loading_changed.emit(False)

    def create_task(self, data: TaskCreate) -> None:
        task = self._service.create(data)
        self._tasks.append(task)
        self.task_created.emit(task)
        self.tasks_changed.emit(self._tasks)

    def delete_task(self, id: int) -> None:
        if self._service.delete(id):
            self._tasks = [t for t in self._tasks if t.id != id]
            self.task_deleted.emit(id)
            self.tasks_changed.emit(self._tasks)

    def update_status(self, id: int, status: TaskStatus) -> None:
        updated = self._service.mark_as(id, status)
        if updated:
            self._tasks = [updated if t.id == id else t for t in self._tasks]
            self.tasks_changed.emit(self._tasks)
```

---

## 9. Views & Components

### 9.1 Main Window

```python
# app/views/main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from app.views.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Ember")
        self.setMinimumSize(1100, 700)
        self._view_cache: dict[str, QWidget] = {}

        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.stack   = QStackedWidget()

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, stretch=1)
        self.setCentralWidget(root)

        self.sidebar.nav_changed.connect(self._navigate)
        self._navigate("dashboard")  # default view

    def _navigate(self, view_key: str) -> None:
        if view_key not in self._view_cache:
            self._view_cache[view_key] = self._build_view(view_key)
            self.stack.addWidget(self._view_cache[view_key])
        self.stack.setCurrentWidget(self._view_cache[view_key])

    def _build_view(self, key: str) -> QWidget:
        """Lazy view initialization — only built on first visit."""
        match key:
            case "dashboard": return self._build_dashboard()
            case "tasks":     return self._build_tasks()
            case "calendar":  return self._build_calendar()
            case _:           raise ValueError(f"Unknown view: {key}")

    # _build_* methods inject dependencies and return the View
```

### 9.2 Task Views Strategy

All four task views receive the **same** `TaskViewModel`. They just render
it differently. This is the Strategy pattern in action.

```python
# app/views/tasks/tasks_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from app.components.view_switcher import ViewSwitcher
from app.viewmodels.task_vm import TaskViewModel


class TasksView(QWidget):
    """
    Parent container for all task view modes.
    Owns the ViewSwitcher and the sub-view stack.
    """
    VIEW_MODES = ["list", "table", "cards", "grid"]

    def __init__(self, vm: TaskViewModel, parent=None) -> None:
        super().__init__(parent)
        self.vm = vm
        self._setup_ui()
        self.vm.tasks_changed.connect(self._on_tasks_changed)
        self.vm.load_tasks()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.switcher = ViewSwitcher(self.VIEW_MODES)
        self.switcher.view_changed.connect(self._switch_view)
        layout.addWidget(self.switcher)
        # stack + lazy sub-views go here

    def _switch_view(self, mode: str) -> None:
        # swap the active sub-view — no data re-fetch
        pass

    def _on_tasks_changed(self, tasks: list) -> None:
        # propagate to current active sub-view
        pass
```

### 9.3 Calendar Views

Each calendar sub-view (`day`, `week`, `month`, `year`) is a standalone
`QWidget` built with `QGridLayout`. **Do not use `QCalendarWidget`** — it
is not styleable enough for Ember's design.

```text
CalendarView (parent)
    ├── ViewSwitcher (day | week | month | year)
    └── QStackedWidget
        ├── DayView    — hour grid, 24 rows
        ├── WeekView   — 7 columns, hour rows
        ├── MonthView  — 6x7 grid, day cells with event dots
        └── YearView   — 12 month mini-grids
```

Each view subscribes to `CalendarViewModel.events_changed` signal.

### 9.4 Dashboard View

Display-only. Reads from `DashboardViewModel` which pulls from
`DashboardService`. Shows:

- Total tasks count
- Tasks by status (bar or ring — keep it simple)
- Tasks due today
- Upcoming events (next 3)
- Last updated tasks

No interactions on the dashboard — it is a **read-only snapshot**.

### 9.5 Reusable Components

| Component | File | Description |
|---|---|---|
| `EmberButton` | `ember_button.py` | Styled QPushButton, variants: primary/ghost/danger |
| `Badge` | `badge.py` | Colored status pill widget |
| `StatWidget` | `stat_widget.py` | Number + label block for dashboard |
| `ViewSwitcher` | `view_switcher.py` | Toggle button group, emits `view_changed` signal |
| `TaskCard` | `task_card.py` | Standalone card for card/grid views |
| `TaskForm` | `task_form.py` | QDialog for create/edit task |

---

## 10. Notifications

Notifications use PySide6's built-in `QSystemTrayIcon` — no extra packages.

```python
# app/services/notification_service.py

from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtCore import QTimer
from app.services.task_service import TaskService


class NotificationService:
    CHECK_INTERVAL_MS = 60_000  # check every 60 seconds

    def __init__(self, tray: QSystemTrayIcon, task_service: TaskService) -> None:
        self._tray         = tray
        self._task_service = task_service
        self._notified_ids: set[int] = set()

        self._timer = QTimer()
        self._timer.timeout.connect(self._check_due_tasks)
        self._timer.start(self.CHECK_INTERVAL_MS)

    def _check_due_tasks(self) -> None:
        due_tasks = self._task_service.get_due_soon(within_minutes=30)
        for task in due_tasks:
            if task.id not in self._notified_ids:
                self._notify(task.title)
                self._notified_ids.add(task.id)

    def _notify(self, title: str) -> None:
        self._tray.showMessage(
            "🔥 Ember",
            f'"{title}" is due soon. Still smoldering?',
            QSystemTrayIcon.MessageIcon.Information,
            4000,
        )
```

> Tray icon setup lives in `main.py`. Pass the `QSystemTrayIcon` instance
> into `NotificationService` at startup.

---

## 11. Styling

### Strategy

- All colors and fonts are defined as Python constants in `theme.py`
- Global structural styles live in `ember.qss`
- Component-specific overrides are applied with `setObjectName()` +
  `#id { }` selectors in the QSS file
- **Never hardcode hex colors in view files** — always import from `theme.py`

### QSS Example

```qss
/* app/styles/ember.qss */

QMainWindow, QWidget {
    background-color: #111111;
    color: #F2F2F2;
    font-family: "Inter";
    font-size: 14px;
}

QPushButton#primary {
    background-color: #FF6524;
    color: #F2F2F2;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
}

QPushButton#primary:hover {
    background-color: #E8311A;
}

QPushButton#ghost {
    background-color: transparent;
    color: #F2F2F2;
    border: 1px solid #2B2B2B;
    border-radius: 6px;
    padding: 8px 16px;
}
```

### Loading Stylesheet

```python
# main.py or MainWindow.__init__

def _load_stylesheet(app: QApplication) -> None:
    qss_path = Path(__file__).parent / "app" / "styles" / "ember.qss"
    with open(qss_path, "r") as f:
        app.setStyleSheet(f.read())
```

---

## 12. Build Order

Follow this order strictly. Each phase depends on the previous.

### Phase 1 — Foundation
```text
[ ] Create project structure and virtual environment
[ ] Install dependencies
[ ] Write app/core/database.py
[ ] Write Task and Event SQLAlchemy models
[ ] Write Pydantic schemas (TaskCreate, TaskRead, TaskUpdate, EventRead...)
[ ] Write BaseRepository + TaskRepository + EventRepository
[ ] Call init_db() and verify ember.db is created
[ ] Set up Alembic for migrations
```

### Phase 2 — Business Logic
```text
[ ] Write TaskService (CRUD + mark_as)
[ ] Write CalendarService (CRUD + get_by_range)
[ ] Write DashboardService (aggregated stats)
[ ] Write NotificationService (due-soon query)
[ ] Write unit tests for all services
```

### Phase 3 — Shell
```text
[ ] Write main.py with QApplication, tray icon, and stylesheet loading
[ ] Write MainWindow with QStackedWidget and lazy view init
[ ] Write Sidebar with nav_changed signal
[ ] Wire sidebar navigation to MainWindow._navigate()
[ ] Verify navigation works with placeholder QLabel views
```

### Phase 4 — Task Views
```text
[ ] Write TaskViewModel
[ ] Write TasksView parent container + ViewSwitcher
[ ] Implement ListView (QListView + basic delegate)
[ ] Implement TableView (QTableView + TaskTableModel)
[ ] Implement CardView (QListView + CardDelegate)
[ ] Implement GridView (custom QWidget grid layout)
[ ] Write TaskForm dialog (create + edit)
[ ] Connect form to TaskViewModel.create_task / update_task
```

### Phase 5 — Dashboard
```text
[ ] Write DashboardViewModel
[ ] Write DashboardView with StatWidgets
[ ] Connect DashboardViewModel signals to DashboardView
[ ] Verify stats update when tasks change
```

### Phase 6 — Calendar
```text
[ ] Write CalendarViewModel
[ ] Write CalendarView parent + ViewSwitcher
[ ] Implement MonthView (6x7 grid, event dots)
[ ] Implement WeekView (7-column, hour rows)
[ ] Implement DayView (24-row hour grid)
[ ] Implement YearView (12 mini month grids)
[ ] Wire CalendarViewModel signals to all calendar sub-views
```

### Phase 7 — Notifications
```text
[ ] Set up QSystemTrayIcon in main.py
[ ] Instantiate NotificationService with tray + task_service
[ ] Test notifications by creating a task due in <30 minutes
```

### Phase 8 — Polish
```text
[ ] Apply ember.qss globally
[ ] Style all components to match design system
[ ] Bundle Inter and JetBrains Mono fonts
[ ] Add app icon (ember.ico)
[ ] Final review of all views on resize / small window sizes
```

---

## 13. Environment Setup

```bash
# Clone the repo
git clone <repo-url>
cd ember

# Create virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Initialize the database
python -c "from app.core.database import init_db; init_db()"

# Run the app
python main.py

# Run tests
pytest tests/
```

---

## 14. Conventions & Rules

### Git

- Commits: conventional commits — `feat:`, `fix:`, `refactor:`, `chore:`
- Push directly to main
- Never commit `ember.db`

### Code Style

- Formatter: `black` (line length 88)
- Type hints: required on all function signatures
- No `Any` unless genuinely unavoidable

### Naming

| Thing | Convention | Example |
|---|---|---|
| Classes | PascalCase | `TaskViewModel` |
| Functions/methods | snake_case | `load_tasks()` |
| Signals | snake_case | `tasks_changed` |
| Constants | UPPER_SNAKE | `CHECK_INTERVAL_MS` |
| Private attrs | `_` prefix | `self._service` |
| QSS object names | lowercase-kebab | `"primary"`, `"ghost"` |

### DO / DO NOT

```text
✅ DO import theme colors from theme.py
✅ DO write signals before slots in ViewModel classes
✅ DO use pydantic schemas as ViewModel ↔ View data transfer objects
✅ DO lazy-init views in MainWindow
✅ DO write a test before fixing any bug

❌ DO NOT access the database from a View or ViewModel directly
❌ DO NOT import PySide6 in services or repositories
❌ DO NOT use QCalendarWidget
❌ DO NOT hardcode colors, sizes, or font names in view files
❌ DO NOT duplicate DB queries — add a method to the repository instead
```

---

## 15. Testing Strategy

### What to Test

| Layer | Tool | What |
|---|---|---|
| Services | `pytest` | All CRUD, edge cases, status transitions |
| Repositories | `pytest` + in-memory SQLite | Query correctness |
| ViewModels | `pytest-qt` | Signal emissions, state changes |
| Views | manual / `pytest-qt` | Smoke tests, form validation |

### In-Memory DB for Tests

```python
# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def task_service(session):
    from app.services.task_service import TaskService
    return TaskService(session)
```

### Example Test

```python
# tests/test_services/test_task_service.py

from app.core.schemas.task import TaskCreate
from app.core.models.task import TaskStatus


def test_create_task(task_service):
    data = TaskCreate(title="Write tests")
    task = task_service.create(data)

    assert task.id is not None
    assert task.title == "Write tests"
    assert task.status == TaskStatus.TODO


def test_mark_as_done(task_service):
    data = TaskCreate(title="Finish feature")
    task = task_service.create(data)

    updated = task_service.mark_as(task.id, TaskStatus.DONE)
    assert updated.status == TaskStatus.DONE
```

---

*Built with PySide6. Powered by stubbornness.*  
*Ember — because your tasks deserve a dramatic metaphor.*
