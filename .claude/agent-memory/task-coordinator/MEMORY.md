# Task Coordinator Agent Memory

## Known Issues & Resolutions

### Issue 1: "Failed to Load Tasks" - 500 Internal Server Error - RESOLVED
**Symptoms**: Frontend shows "Failed to Load Tasks" error, backend returns 500 Internal Server Error
**Root Cause**: Type mismatch in authentication dependency injection
- `get_current_user()` in `/backend/core/security.py` returned a string (user_id from JWT)
- Route handlers in `/backend/routes/tasks.py` expected a User object with `.id` attribute
- Code tried to access `current_user.id` when `current_user` was already a string: `AttributeError: 'str' object has no attribute 'id'`

**Resolution** (2026-02-06):
1. Updated all route handlers in `/backend/routes/tasks.py` to accept `current_user_id: str` instead of `current_user: User`
2. Removed `.id` attribute access since the dependency already returns the user_id string
3. Removed unused `User` import from routes/tasks.py
4. Updated parameter names to be more explicit: `current_user_id` instead of `current_user`
5. Enhanced logging: DEBUG level with format string in main.py, exception logging in routes

**Files Modified**:
- `/backend/routes/tasks.py` - Lines 19, 45-56, 72, 89-91, 103, 120-122, 143, 161-166, 198, 212-214
- `/backend/main.py` - Enhanced logging configuration

**Testing Verification**:
- GET /api/tasks returns `{"tasks":[],"total":0,"page":1,"page_size":20}` for new users
- POST /api/tasks successfully creates tasks with all fields
- GET /api/tasks returns created tasks with proper pagination
- User isolation working correctly (tasks filtered by JWT user_id)

### Previous Issues (Already Fixed):
**AuthContext not setting user state**: Updated to decode JWT on mount
**Database missing priority column**: Migration 001_add_task_fields.sql applied
**Database enum case sensitivity**: Constraints use `LOWER()` for case-insensitive checks

### Issue 2: Multiple Auth Service Implementations
**Location**: Three auth service files with inconsistent implementations
- `auth-service.ts` - Uses fetch API directly
- `auth.service.ts` - Uses axios with interceptors
- `auth-api-service.ts` - Another fetch implementation

**Impact**: AuthContext uses `auth.service.ts` while other components may use different services
**Recommendation**: Consolidate to single auth service (prefer axios-based for interceptors)

## API Endpoint Patterns

### Tasks Endpoint
- **GET** `/api/tasks` - Returns `{tasks: [], total: 0, page: 1, page_size: 20}`
- **POST** `/api/tasks` - Requires: `{title, description?, status?, priority?}`
- **Auth**: Bearer token required in `Authorization` header
- **User Isolation**: Backend automatically filters by JWT `sub` claim

### Auth Endpoints
- **POST** `/auth/register` - Returns user object + tokens
- **POST** `/auth/login` - Returns tokens only
- **Response Format**: `{access_token, refresh_token, token_type: "bearer"}`

## Database Schema Notes

### Tasks Table Columns
- `id` (UUID, primary key)
- `user_id` (string, indexed)
- `title` (varchar 255, required)
- `description` (varchar 1000, optional)
- `status` (varchar, constraint: pending|in_progress|completed)
- `priority` (varchar 10, constraint: low|medium|high|urgent)
- `due_date` (timestamp, nullable)
- `completed_at` (timestamp, nullable)
- `is_deleted` (boolean, default false, indexed)
- `created_at` (timestamp with timezone)
- `updated_at` (timestamp with timezone)

**Important**: Constraints use `LOWER()` to handle both lowercase and uppercase enum values from SQLModel

## Common Failure Modes

### 1. Token Not Persisting
- Check `localStorage.getItem('access_token')` in browser console
- Verify AuthContext `getAccessToken()` returns non-null
- Check token expiry: decode JWT and compare `exp` with current timestamp

### 2. API Returns 401
- Token missing from request headers
- Token expired (check `exp` claim)
- Refresh token flow not working (check axios interceptor in `/services/api.ts`)

### 3. API Returns 500 with Type Errors
- Check dependency injection types match expected types in route handlers
- Verify User vs string user_id consistency across all endpoints
- Check that attributes accessed on dependencies actually exist
- Use `logger.exception()` to get full traceback in logs

### 4. API Returns 500 with Database Error
- Column missing from database (run migrations)
- Constraint violation (check enum values match constraints)
- Connection pool exhausted (check backend logs)

## Performance Characteristics

### Task Load Times (Measured)
- Empty task list: ~50ms (backend) + ~100ms (network)
- First load with 20 tasks: ~150ms (includes query time)
- Token decode (frontend): <5ms

### Optimization Opportunities
1. Implement optimistic UI updates for task creation
2. Add debouncing to rapid task updates
3. Consider WebSocket for real-time task sync
4. Cache task list in React Query with stale-while-revalidate

## State Management Patterns

### TaskProvider Context
- **Location**: `/frontend/src/services/task-service.tsx`
- **State**: `{tasks: Task[], loading: boolean, error: string | null}`
- **Fetches on Mount**: useEffect in TaskProvider calls `fetchTasks()`
- **Error Handling**: Sets error state, displays in UI, allows retry

### AuthContext
- **Location**: `/frontend/src/contexts/AuthContext.tsx`
- **State**: `{user: User | null, loading: boolean}`
- **Token Storage**: localStorage (keys: `access_token`, `refresh_token`)
- **Auto-refresh**: Axios interceptor handles 401 responses

## Testing Notes

### Manual API Testing
```bash
# Register new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Get tasks (replace TOKEN, use single quotes to preserve token)
curl -H 'Authorization: Bearer TOKEN' \
  http://localhost:8000/api/tasks

# Create task (use single quotes for auth header)
curl -X POST -H 'Authorization: Bearer TOKEN' \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Testing","status":"pending","priority":"medium"}' \
  http://localhost:8000/api/tasks
```

**IMPORTANT**: Always use single quotes around Authorization header to preserve token value in shell.

### Test HTML Tool
- Created `/frontend/test-api-flow.html` for browser-based API testing
- Tests: register, login, fetch tasks, create task, token decode
- Open in browser after starting frontend dev server

## Migration History

### 001_add_task_fields.sql
- Adds: priority, due_date, completed_at, is_deleted columns
- Creates indexes: user_id+status, user_id+due_date, user_id+is_deleted
- Adds constraints with case-insensitive checks

### 002_create_task_reminders.sql
- Creates task_reminders table for notification system
- Not yet affecting task load flow

## Architecture Patterns

### Dependency Injection (FastAPI)
- **Pattern**: FastAPI's `Depends()` for session and authentication
- **get_current_user**: Returns string user_id (extracted from JWT `sub` claim)
- **get_session**: Yields SQLModel Session with connection pooling
- **CRITICAL**: Route handler parameter types must match dependency return types exactly
  - If dependency returns `str`, handler must accept `str` (not `User`)
  - If dependency returns `User`, handler must accept `User` (not `str`)

### Error Handling Standards
- All routes use try-except with HTTPException
- Use `logger.exception()` for ERROR level (includes full traceback)
- Use `logger.debug()` for operation flow tracing
- Consistent error response format: `{"detail": "error message"}`
- Set logging level to DEBUG in main.py for detailed troubleshooting

### User Isolation Pattern
- JWT token contains user_id in `sub` claim
- All database queries filter by user_id from token (not from request body)
- Never accept user_id from request parameters (security requirement)
- UUID normalization to lowercase for comparison (handle string representation differences)
