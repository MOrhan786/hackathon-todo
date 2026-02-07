-- Rollback Script: Revert schema changes back to VARCHAR types
-- Use this if the proper fix causes issues

-- PART 1: Rollback user_id to VARCHAR
-- =====================================

-- Drop foreign key constraint
ALTER TABLE tasks DROP CONSTRAINT IF EXISTS fk_tasks_user_id;

-- Add new VARCHAR column
ALTER TABLE tasks ADD COLUMN user_id_old VARCHAR;

-- Convert UUID back to string
UPDATE tasks
SET user_id_old = user_id::text;

-- Drop UUID column and rename old one
ALTER TABLE tasks DROP COLUMN user_id;
ALTER TABLE tasks RENAME COLUMN user_id_old TO user_id;

-- Make it NOT NULL
ALTER TABLE tasks ALTER COLUMN user_id SET NOT NULL;

-- PART 2: Rollback ENUM types to VARCHAR
-- ========================================

-- Convert status back to VARCHAR
ALTER TABLE tasks
ALTER COLUMN status TYPE VARCHAR
USING status::text;

-- Convert priority back to VARCHAR
ALTER TABLE tasks
ALTER COLUMN priority TYPE VARCHAR
USING priority::text;

-- Drop the ENUM types
DROP TYPE IF EXISTS taskstatus CASCADE;
DROP TYPE IF EXISTS taskpriority CASCADE;

-- PART 3: Drop performance indexes
-- =================================

DROP INDEX IF EXISTS idx_tasks_user_id;
DROP INDEX IF EXISTS idx_tasks_user_status_active;
DROP INDEX IF EXISTS idx_tasks_due_date;
DROP INDEX IF EXISTS idx_tasks_user_priority;

-- PART 4: Verification
-- ====================

SELECT
    column_name,
    data_type,
    udt_name
FROM information_schema.columns
WHERE table_name = 'tasks'
ORDER BY ordinal_position;
