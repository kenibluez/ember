# Ember Database & Migration Guide

## 1. Initializing the Database
Before running migrations, ensure your database file is created.
\`\`\`bash
python -c "from app.core.database import init_db; init_db()"
\`\`\`

## 2. Alembic Migrations
Alembic tracks changes to your SQLAlchemy models and updates the SQLite schema.

**Generate a new migration:**
Run this whenever you change `models/task.py` or `models/event.py`.
\`\`\`bash
alembic revision --autogenerate -m "describe_your_changes_here"
\`\`\`

**Apply migrations (Update Database):**
Run this to apply the generated schema changes to `ember.db`.
\`\`\`bash
alembic upgrade head
\`\`\`

**Rollback a migration:**
If you made a mistake and need to undo the last applied migration.
\`\`\`bash
alembic downgrade -1
\`\`\`

## 3. Seeding Data
Run the seed script to populate the database with initial test data. Ensure you have applied the base migrations first.
\`\`\`bash
python seed.py
\`\`\`
