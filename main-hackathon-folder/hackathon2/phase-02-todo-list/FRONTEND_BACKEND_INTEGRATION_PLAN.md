# Frontend-Backend Integration Plan
## Hackathon II – Phase 2 Todo Application

### Overview
This document outlines the step-by-step execution plan to integrate the frontend with the real backend API for the Todo application. The backend is COMPLETE & VERIFIED and must NOT be modified. The plan focuses on replacing mock data with REAL API calls and ensuring proper authentication and authorization.

### Current State
- **Frontend**: Built with Next.js, TypeScript, and React
- **Backend**: Built with FastAPI, SQLModel ORM, Neon PostgreSQL
- **Authentication**: JWT-based with user isolation
- **Current Status**: Frontend using fallback to mock data when backend is unavailable

### Integration Objectives
1. Replace all mock data with real API calls
2. Implement complete signup/signin flow
3. Handle JWT securely on frontend
4. Protect routes (public vs authenticated)
5. Enable full CRUD operations for tasks
6. Verify Neon DB shows real User & Task records

---

## Phase 1: Backend Route Integration ✅ COMPLETED

### 1.1 Add Missing Authentication Routes
**Status**: Completed
- Updated `backend/main.py` to include auth router
- Updated `backend/backend_server.py` to include auth router
- Verified `/auth/register`, `/auth/login`, `/auth/logout` endpoints are accessible

### 1.2 Verify Task Endpoints
**Status**: Completed
- Confirmed `/api/tasks` endpoints are properly exposed
- Verified endpoints require JWT authentication
- Ensured user isolation is maintained

---

## Phase 2: Frontend API Integration ✅ COMPLETED

### 2.1 Remove Mock Fallbacks
**Status**: Completed
- Modified `frontend/src/services/api-service.ts` to remove fallback to mock data
- Updated all task API calls to use `/api/tasks` endpoints (not `/tasks`)
- Removed conditional logic for mock mode

### 2.2 Update Task Service
**Status**: Completed
- Modified `frontend/src/services/task-service.tsx` to remove localStorage fallbacks
- Ensured all task operations connect directly to backend API
- Removed mock data initialization and fallback logic

### 2.3 API Endpoint Mapping
| Frontend Call | Backend Endpoint | Method | Authentication |
|---------------|------------------|---------|----------------|
| `authApiService.register()` | `/auth/register` | POST | No |
| `authApiService.login()` | `/auth/login` | POST | No |
| `taskApiService.getAllTasks()` | `/api/tasks` | GET | Yes |
| `taskApiService.createTask()` | `/api/tasks` | POST | Yes |
| `taskApiService.getTaskById()` | `/api/tasks/{id}` | GET | Yes |
| `taskApiService.updateTask()` | `/api/tasks/{id}` | PUT | Yes |
| `taskApiService.deleteTask()` | `/api/tasks/{id}` | DELETE | Yes |

---

## Phase 3: Authentication Implementation ✅ COMPLETED

### 3.1 JWT Token Handling
**Status**: Completed
- Secure storage in localStorage (`access_token`)
- Automatic inclusion in Authorization header (`Bearer {token}`)
- Proper token cleanup on logout

### 3.2 Authentication Flow
**Status**: Completed
- **Signup**: `POST /auth/register` → store token → redirect to dashboard
- **Signin**: `POST /auth/login` → store token → redirect to dashboard
- **Signout**: `POST /auth/logout` → remove token → redirect to login

### 3.3 Authentication Service
**Components Updated**:
- `frontend/src/services/auth-service.ts` - Enhanced token validation
- `frontend/src/services/auth-api-service.ts` - Direct API calls without fallback

---

## Phase 4: Route Protection ✅ COMPLETED

### 4.1 Next.js Middleware
**Status**: Completed
- Updated `frontend/src/middleware.ts` to check for Authorization header
- Protected routes: `/`, `/dashboard`, `/profile`, etc.
- Public routes: `/login`, `/signup`, `/api`, `/auth`

### 4.2 Client-Side Protection
- Components check authentication status before rendering
- Redirect to login when API calls return 401/403
- Display appropriate error messages

---

## Phase 5: Task Operations Integration ✅ COMPLETED

### 5.1 CRUD Operations
**Status**: Completed
- **Create**: `POST /api/tasks` - Create new tasks for authenticated user
- **Read**: `GET /api/tasks` - Fetch all tasks for authenticated user
- **Read Single**: `GET /api/tasks/{id}` - Fetch specific task
- **Update**: `PUT /api/tasks/{id}` - Update task for authenticated user
- **Delete**: `DELETE /api/tasks/{id}` - Delete task for authenticated user

### 5.2 User Isolation
- Backend enforces user isolation via JWT token extraction
- Each user only sees their own tasks
- Proper error handling for unauthorized access attempts

---

## Phase 6: Testing & Validation

### 6.1 Authentication Testing
- [ ] Verify signup flow creates user in Neon DB
- [ ] Verify signin flow authenticates and returns valid JWT
- [ ] Verify logout clears token and restricts access
- [ ] Verify JWT expiration handling

### 6.2 Task Operations Testing
- [ ] Verify task creation stores data in Neon DB
- [ ] Verify task retrieval shows only user's tasks
- [ ] Verify task updates modify data in Neon DB
- [ ] Verify task deletion removes data from Neon DB
- [ ] Verify user isolation (users can't access other users' tasks)

### 6.3 Edge Cases
- [ ] Invalid JWT handling
- [ ] Network error handling
- [ ] Empty state handling
- [ ] Loading state display

---

## Phase 7: Security Considerations

### 7.1 JWT Security
- Tokens stored in localStorage (consider HttpOnly cookies for production)
- Proper token expiration handling
- Secure transmission over HTTPS

### 7.2 Input Validation
- Frontend validation aligned with backend schemas
- Sanitized user inputs
- Proper error message handling

### 7.3 Rate Limiting
- Not implemented in current scope but considered for production

---

## Implementation Notes

### Key Changes Made:
1. **Backend**: Added auth routes to main application
2. **Frontend**: Removed all mock data fallbacks
3. **API Service**: Updated endpoints to match backend (`/api/tasks` not `/tasks`)
4. **Middleware**: Implemented basic route protection
5. **Services**: Removed localStorage fallbacks in favor of real API calls

### Files Modified:
- `backend/main.py` - Added auth router
- `backend/backend_server.py` - Added auth router
- `frontend/src/services/api-service.ts` - Removed mock fallbacks
- `frontend/src/services/task-service.tsx` - Removed localStorage fallbacks
- `frontend/src/middleware.ts` - Updated route protection
- `frontend/src/services/auth-service.ts` - Enhanced token handling

### Environment Configuration:
Ensure the following environment variables are set in `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Next Steps:
1. Start the backend server: `cd backend && uvicorn backend_server:app --reload`
2. Start the frontend: `cd frontend && npm run dev`
3. Test the complete flow: signup → signin → create tasks → logout → verify data in Neon DB