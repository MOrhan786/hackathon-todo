-- Quick Fix: Normalize enum data to lowercase
-- This will fix the immediate 500 error by ensuring all status/priority values match the model

-- Backup current data (optional, but recommended)
-- CREATE TABLE tasks_backup AS SELECT * FROM tasks;

-- Normalize status values to lowercase
UPDATE tasks
SET status = LOWER(status)
WHERE status != LOWER(status);

-- Fix the specific 'in_progress' case (IN_PROGRESS -> in_progress)
UPDATE tasks
SET status = 'in_progress'
WHERE status IN ('IN_PROGRESS', 'In_Progress');

-- Normalize priority values to lowercase
UPDATE tasks
SET priority = LOWER(priority)
WHERE priority != LOWER(priority);

-- Drop the unused ENUM types that are causing confusion
DROP TYPE IF EXISTS taskstatus CASCADE;
DROP TYPE IF EXISTS taskpriority CASCADE;

-- Verify the changes
SELECT
    'status' as column_name,
    status as value,
    COUNT(*) as count
FROM tasks
GROUP BY status
UNION ALL
SELECT
    'priority' as column_name,
    priority as value,
    COUNT(*) as count
FROM tasks
GROUP BY priority
ORDER BY column_name, value;
