-- Migration 002: Create task_reminders table
-- Run this migration to add reminder functionality

-- Create task_reminders table
CREATE TABLE IF NOT EXISTS task_reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL,
    remind_at TIMESTAMP NOT NULL,
    is_sent BOOLEAN NOT NULL DEFAULT false,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- Add indexes for improved query performance
CREATE INDEX IF NOT EXISTS idx_reminder_task ON task_reminders(task_id);
CREATE INDEX IF NOT EXISTS idx_reminder_user ON task_reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_reminder_pending ON task_reminders(is_sent, remind_at);
CREATE INDEX IF NOT EXISTS idx_reminder_user_task ON task_reminders(user_id, task_id);
