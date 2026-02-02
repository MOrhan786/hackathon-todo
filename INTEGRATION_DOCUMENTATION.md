# Frontend-Backend Integration Documentation
## Hackathon II – Phase 2 Todo Application

### Overview
This document provides comprehensive documentation for the frontend-backend integration of the Todo application. The backend is COMPLETE & VERIFIED from the 001-backend-api branch, and this document covers how the frontend integrates with it.

### Architecture Overview

#### Backend API Structure
The backend provides a secure API with JWT-based authentication:

**Authentication Endpoints:**
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `POST /auth/logout` - User logout

**Task Endpoints:**
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create a new task for authenticated user
- `GET /api/tasks/{id}` - Get a specific task by ID
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task

#### Frontend Architecture
The frontend is built with Next.js and follows a service-oriented architecture:

**Key Services:**
- `api-service.ts` - Low-level API communication layer
- `task-service.tsx` - Business logic for task operations
- `auth-api-service.ts` - Authentication API calls
- `auth-service.ts` - Authentication business logic

### Integration Details

#### 1. Authentication Flow

**Registration Flow:**
1. User fills registration form on `/signup`
2. `authService.register()` is called
3. Makes POST request to `/auth/register`
4. Backend creates user and returns JWT token
5. Token is stored in localStorage
6. User is redirected to dashboard (`/`)

**Login Flow:**
1. User fills login form on `/login`
2. `authService.login()` is called
3. Makes POST request to `/auth/login`
4. Backend validates credentials and returns JWT token
5. Token is stored in localStorage
6. User is redirected to dashboard (`/`)

**Logout Flow:**
1. User clicks logout button
2. `authService.logout()` is called
3. Makes POST request to `/auth/logout`
4. Token is removed from localStorage
5. User is redirected to login page

#### 2. JWT Token Management

**Storage:**
- JWT tokens are stored in browser localStorage under key `access_token`
- Tokens are automatically included in Authorization header for API requests
- Token validity is checked before API calls

**Security:**
- Tokens are sent as `Bearer {token}` in Authorization header
- Token expiration is validated client-side
- Invalid tokens result in redirect to login

#### 3. Task Operations

**Task Creation:**
```typescript
// Using the service
await taskService.createTask({
  title: "New task",
  description: "Task description",
  completed: false
});
```

**Task Retrieval:**
```typescript
// Get all tasks for authenticated user
const tasks = await taskService.getAllTasks();
```

**Task Updates:**
```typescript
// Update specific task
await taskService.updateTask(taskId, {
  title: "Updated title",
  completed: true
});
```

**Task Deletion:**
```typescript
// Delete specific task
await taskService.deleteTask(taskId);
```

#### 4. Route Protection

**Next.js Middleware (`middleware.ts`):**
- Protects routes that require authentication
- Public routes: `/login`, `/signup`, `/api`, `/auth`
- Protected routes: `/`, `/dashboard`, etc.
- Checks for Authorization header presence

**Client-Side Protection:**
- Dashboard page checks authentication status
- Redirects unauthenticated users to login
- Handles authentication state changes

### Error Handling

#### API Error Handling
- Network errors are caught and displayed to user
- HTTP status codes are properly handled
- Specific error messages are shown for different error types
- Graceful degradation when API is unavailable

#### Authentication Error Handling
- Invalid credentials show specific error messages
- Expired tokens redirect to login
- Unauthorized access attempts are handled gracefully

### Data Flow

#### User Data Flow
1. User interacts with UI components
2. React hooks trigger service methods
3. Services make API calls to backend
4. Backend processes requests and returns data
5. Services update React state via context
6. UI components re-render with new data

#### Task Data Flow
1. User creates/updates/deletes tasks via UI
2. Task service methods are called
3. API service makes authenticated requests to backend
4. Backend validates JWT and user permissions
5. Database operations are performed
6. Updated data is returned to frontend
7. React context updates state
8. UI reflects changes

### Security Considerations

#### JWT Security
- Tokens are validated both client-side and server-side
- User ID is extracted from JWT payload on backend
- All task operations are filtered by authenticated user
- Cross-user access is prevented

#### Input Validation
- Client-side validation mirrors backend validation
- User inputs are sanitized before API calls
- Error messages are user-friendly but informative

#### Data Isolation
- Each user only sees their own tasks
- Backend enforces user isolation at database level
- Unauthorized access attempts return 403 Forbidden

### Testing Approach

#### Manual Testing
- Complete user flow (register → login → create tasks → logout)
- Multiple user isolation testing
- Error scenario testing
- Authentication timeout handling

#### Automated Testing
- Integration test script provided (`test_integration.sh`)
- API endpoint verification
- User isolation validation
- Error condition testing

### Environment Configuration

#### Frontend Environment Variables
```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend Environment Variables
```bash
# backend/.env
DATABASE_URL=your_neon_db_url
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Deployment Considerations

#### Production Setup
- Use HTTPS for secure token transmission
- Consider HttpOnly cookies instead of localStorage for production
- Implement proper logging and monitoring
- Set up proper CORS policies

#### Database
- Neon Serverless PostgreSQL handles scaling automatically
- Connection pooling is managed by SQLModel/SQLAlchemy
- Database migrations are handled on startup

### Troubleshooting

#### Common Issues
1. **Token not persisting**: Check localStorage access
2. **API calls failing**: Verify backend URL and network connectivity
3. **Authentication not working**: Check JWT token format and expiration
4. **User isolation not working**: Verify backend authentication middleware

#### Debugging Steps
1. Check browser developer tools for network errors
2. Verify backend is running and accessible
3. Confirm JWT token is present in localStorage
4. Validate Authorization header format in API calls

### Future Enhancements

#### Security Improvements
- Implement refresh token rotation
- Add rate limiting
- Consider HttpOnly cookies for token storage
- Implement additional input sanitization

#### Performance Optimizations
- Add caching layers
- Implement optimistic updates
- Add pagination for large task lists
- Optimize database queries

#### User Experience
- Add loading states and progress indicators
- Implement undo functionality for task deletion
- Add bulk operations
- Improve error messaging and recovery

### Conclusion

The frontend-backend integration is complete and functioning as designed. All objectives have been met:

✅ Mock data replaced with real API calls
✅ Complete signup/signin flow implemented
✅ JWT securely handled on frontend
✅ Routes properly protected
✅ Full CRUD operations for tasks
✅ Neon DB shows real User & Task records
✅ User isolation enforced

The system is ready for production use with the security and functionality required for a multi-user todo application.