"""
Migration script for Phase 5: Add new columns to tasks table.
Adds: tags, is_recurring, recurrence_pattern, recurrence_interval,
      recurrence_end_date, reminder_at, reminder_sent, parent_task_id
"""

from core.db import engine
from sqlalchemy import text

MIGRATIONS = [
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS tags JSON DEFAULT '[]'",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(20) DEFAULT NULL",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_interval INTEGER DEFAULT 1",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_end_date TIMESTAMP WITH TIME ZONE DEFAULT NULL",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_at TIMESTAMP WITH TIME ZONE DEFAULT NULL",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_sent BOOLEAN DEFAULT FALSE",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS parent_task_id UUID DEFAULT NULL",
]

def run_migration():
    print("Running Phase 5 migration...")
    with engine.connect() as conn:
        for sql in MIGRATIONS:
            try:
                conn.execute(text(sql))
                print(f"  OK: {sql[:60]}...")
            except Exception as e:
                print(f"  SKIP: {sql[:60]}... ({e})")
        conn.commit()
    print("Migration complete!")

if __name__ == "__main__":
    run_migration()
