-- Proper Schema Migration: Fix all type inconsistencies
-- This is the recommended long-term solution

-- PART 1: Fix enum data and create proper ENUM types
-- ====================================================

-- Normalize existing data first
UPDATE tasks SET status = LOWER(status);
UPDATE tasks SET status = 'in_progress' WHERE status = 'in_progress';
UPDATE tasks SET priority = LOWER(priority);

-- Drop old enum types if they exist
DROP TYPE IF EXISTS taskstatus CASCADE;
DROP TYPE IF EXISTS taskpriority CASCADE;

-- Create ENUM types with correct lowercase values
CREATE TYPE taskstatus AS ENUM ('pending', 'in_progress', 'completed');
CREATE TYPE taskpriority AS ENUM ('low', 'medium', 'high', 'urgent');

-- Alter columns to use ENUM types
ALTER TABLE tasks
ALTER COLUMN status TYPE taskstatus
USING status::taskstatus;

ALTER TABLE tasks
ALTER COLUMN priority TYPE taskpriority
USING priority::taskpriority;

-- PART 2: Fix user_id to use UUID type
-- =====================================

-- Add new UUID column
ALTER TABLE tasks ADD COLUMN user_id_new UUID;

-- Convert existing string UUIDs to proper UUID type
UPDATE tasks
SET user_id_new = user_id::uuid;

-- Verify all conversions succeeded
DO $$
DECLARE
    null_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO null_count
    FROM tasks
    WHERE user_id_new IS NULL;

    IF null_count > 0 THEN
        RAISE EXCEPTION 'UUID conversion failed for % rows', null_count;
    END IF;
END $$;

-- Drop old column and rename new one
ALTER TABLE tasks DROP COLUMN user_id;
ALTER TABLE tasks RENAME COLUMN user_id_new TO user_id;

-- Make it NOT NULL
ALTER TABLE tasks ALTER COLUMN user_id SET NOT NULL;

-- Add foreign key constraint for referential integrity
ALTER TABLE tasks
ADD CONSTRAINT fk_tasks_user_id
FOREIGN KEY (user_id)
REFERENCES "user"(id)
ON DELETE CASCADE;

-- PART 3: Add indexes for performance
-- ====================================

-- Index on user_id for filtering tasks by user
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Composite index for common query pattern (user + status + not deleted)
CREATE INDEX idx_tasks_user_status_active
ON tasks(user_id, status, is_deleted)
WHERE is_deleted = false;

-- Index for due date queries
CREATE INDEX idx_tasks_due_date
ON tasks(due_date)
WHERE due_date IS NOT NULL AND is_deleted = false;

-- Index for priority queries
CREATE INDEX idx_tasks_user_priority
ON tasks(user_id, priority)
WHERE is_deleted = false;

-- PART 4: Verification
-- ====================

-- Check schema
SELECT
    column_name,
    data_type,
    udt_name,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'tasks'
ORDER BY ordinal_position;

-- Check constraints
SELECT
    conname as constraint_name,
    contype as constraint_type
FROM pg_constraint
WHERE conrelid = 'tasks'::regclass;

-- Check indexes
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'tasks';

-- Count tasks to ensure no data loss
SELECT COUNT(*) as total_tasks FROM tasks;
