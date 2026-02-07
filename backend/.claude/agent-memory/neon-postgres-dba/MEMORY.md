# Neon PostgreSQL DBA - Agent Memory

## Project: Todo List Application Backend

### Database Configuration
- **Platform**: Neon Serverless PostgreSQL
- **Connection**: Pooled connection via Neon proxy
- **Schema**: `public`
- **ORM**: SQLModel (built on SQLAlchemy)

### Critical Issues Found (2026-02-07)

#### 1. Enum Type Mismatch
**Problem**: Status and priority columns stored as VARCHAR with mixed-case values, but model expects lowercase enum values.
- Database ENUM type `taskstatus` exists but isn't used by the column
- Data contains: `'PENDING'`, `'pending'`, `'completed'` (mixed case)
- Model expects: `'pending'`, `'in_progress'`, `'completed'` (lowercase)
- **Fix**: Normalize data to lowercase, remove unused ENUM types

#### 2. User ID Type Inconsistency
**Problem**: `tasks.user_id` is VARCHAR, but `user.id` is UUID
- No foreign key constraint = no referential integrity
- String comparisons instead of UUID comparisons (performance impact)
- **Recommended**: Migrate user_id to UUID type with FK constraint

### Schema Patterns

#### Tasks Table
- Primary key: `id` (UUID)
- Soft delete: `is_deleted` (boolean, indexed)
- Timestamps: `created_at`, `updated_at` (with timezone)
- User isolation: All queries must filter by `user_id`

#### Users Table
- Primary key: `id` (UUID)
- Unique constraint: `email`
- Password stored as: `password_hash` (bcrypt)

### Common Query Patterns
1. Get tasks by user: `WHERE user_id = ? AND is_deleted = false`
2. Filter by status: Add `AND status = ?`
3. Pagination: Use `OFFSET` and `LIMIT`

### Index Strategy (Post-Migration)
```sql
-- User isolation (most common query)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- User + status filtering
CREATE INDEX idx_tasks_user_status_active
ON tasks(user_id, status, is_deleted)
WHERE is_deleted = false;

-- Due date queries
CREATE INDEX idx_tasks_due_date ON tasks(due_date)
WHERE due_date IS NOT NULL AND is_deleted = false;
```

### Migration Files Created
- `migrations/quick_fix_enum_data.sql` - Emergency fix for 500 error
- `migrations/proper_fix_schema.sql` - Complete schema normalization
- `migrations/rollback_proper_fix.sql` - Rollback script
- `apply_quick_fix.py` - Python script to apply quick fix

### Neon-Specific Considerations
- Connection pooling via Neon proxy (already configured in DATABASE_URL)
- Autoscaling compute: Keep queries efficient to minimize cold starts
- Branching: Test migrations on Neon branches before applying to main
- Point-in-time recovery: Available for disaster recovery

### Best Practices for This Project
1. Always filter by `user_id` for user isolation
2. Use soft deletes (`is_deleted = false`)
3. Normalize enum values to lowercase before storage
4. Use UUID for all ID fields
5. Add FK constraints for data integrity
6. Index on user_id + common filter columns

### Known Technical Debt
1. Missing foreign key constraint: tasks.user_id -> user.id
2. VARCHAR enum columns should be PostgreSQL ENUM types
3. Missing composite indexes for common query patterns
4. No database-level audit logging
