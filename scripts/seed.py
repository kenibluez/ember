import os
import sys
from datetime import UTC, datetime, timedelta

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, init_db
from app.core.models.event import Event
from app.core.models.task import Task, TaskPriority, TaskStatus


def seed_data():
    # Ensure tables are created
    init_db()

    db = SessionLocal()

    # Check if data already exists to prevent duplicates
    if db.query(Task).first() or db.query(Event).first():
        print("Database already seeded. Skipping.")
        return

    now = datetime.now(UTC)

    # --- Seed Tasks ---
    tasks = [
        Task(
            title="Draft UNIX vs Windows OS Abstraction Report",
            description="Focus on process creation and storage philosophies.",
            status=TaskStatus.DONE,
            priority=TaskPriority.HIGH,
            due_date=now - timedelta(days=2),
        ),
        Task(
            title="Implement WAT Bubble Sort logic",
            description="Handle linear memory and stack-based execution in WebAssembly.",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            due_date=now + timedelta(hours=2),
        ),
        Task(
            title="Automate Screeps Lab Manager",
            description="Use global reactions constant for mineral synthesis.",
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            due_date=now + timedelta(days=1),
        ),
        Task(
            title="Curate 'Savoir Faire' playlist",
            description="Cinematic noir vibes only.",
            status=TaskStatus.TODO,
            priority=TaskPriority.LOW,
            due_date=None,
        ),
        Task(
            title="Cancel test task",
            status=TaskStatus.CANCELLED,
            priority=TaskPriority.LOW,
        ),
    ]

    # --- Seed Events ---
    events = [
        Event(
            title="ESET Business Meets – 5th Edition",
            description="Logistics team duties / aide-de-camp at Keiser Managua campus.",
            start_dt=now + timedelta(days=1, hours=8),  # Starts tomorrow at 8 AM
            end_dt=now + timedelta(days=1, hours=17),  # Ends tomorrow at 5 PM
            all_day=True,
        ),
        Event(
            title="Software Engineering Lecture",
            description="Senior I class.",
            start_dt=now - timedelta(days=1, hours=2),  # Happened yesterday
            end_dt=now - timedelta(days=1, hours=0),
            all_day=False,
        ),
        Event(
            title="KaplayJS Game Dev Sprint",
            description="Work on the 'Icy' puzzle-platformer mechanics.",
            start_dt=now + timedelta(hours=3),  # Happens in 3 hours
            end_dt=now + timedelta(hours=6),
            all_day=False,
        ),
    ]

    db.add_all(tasks)
    db.add_all(events)
    db.commit()
    print("Database seeded successfully with tasks and events! 🔥")


if __name__ == "__main__":
    seed_data()
