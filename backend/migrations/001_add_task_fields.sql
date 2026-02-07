-- Migration 001: Add new fields to tasks table
-- Run this migration to add priority, due_date, completed_at, and is_deleted fields

-- Add new columns to tasks table
ALTER TABLE tasks
    ADD COLUMN IF NOT EXISTS priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    ADD COLUMN IF NOT EXISTS due_date TIMESTAMP NULL,
    ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP NULL,
    ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN NOT NULL DEFAULT false;

-- Update status column to allow 'in_progress' value
-- Note: If constraint exists, drop it first
ALTER TABLE tasks
    DROP CONSTRAINT IF EXISTS chk_task_status;

-- Add updated status constraint (case-insensitive to support SQLModel enum values)
ALTER TABLE tasks
    ADD CONSTRAINT chk_task_status
    CHECK (LOWER(status) IN ('pending', 'in_progress', 'completed'));

-- Add priority constraint (case-insensitive to support SQLModel enum values)
ALTER TABLE tasks
    DROP CONSTRAINT IF EXISTS chk_task_priority;
ALTER TABLE tasks
    ADD CONSTRAINT chk_task_priority
    CHECK (LOWER(priority) IN ('low', 'medium', 'high', 'urgent'));

-- Add indexes for improved query performance
CREATE INDEX IF NOT EXISTS idx_task_user_status ON tasks(user_id, status);
CREATE INDEX IF NOT EXISTS idx_task_user_due ON tasks(user_id, due_date);
CREATE INDEX IF NOT EXISTS idx_task_user_deleted ON tasks(user_id, is_deleted);
