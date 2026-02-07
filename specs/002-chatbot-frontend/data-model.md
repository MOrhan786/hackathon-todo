# Data Model: Frontend State Management

**Feature**: 002-chatbot-frontend
**Date**: 2026-02-06
**Purpose**: Define TypeScript types and state models for the chatbot frontend

## Overview

The frontend state model consists of:
1. **API Entity Types** - Mirror backend models (User, Task, ChatMessage)
2. **Component State Types** - UI-specific state (loading, errors, form data)
3. **Context State Types** - Global application state (AuthContext)

All types are defined in `/frontend/types/` directory using TypeScript interfaces and types.

## Entity Type Definitions

### User

Represents an authenticated user account.

```typescript
// types/auth.types.ts

export interface User {
  id: string;               // UUID as string
  email: string;            // User's email address
  created_at: string;       // ISO 8601 timestamp
  updated_at: string;       // ISO 8601 timestamp
}

export interface AuthTokens {
  access_token: string;     // JWT access token
  refresh_token: string;    // JWT refresh token
  token_type: 'bearer';     // Always "bearer"
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginResponse extends User {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}

export interface RegisterResponse extends LoginResponse {
  // Same as LoginResponse (backend returns tokens on registration)
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: 'bearer';
}
```

**Validation Rules**:
- Email: Must be valid email format (RFC 5322)
- Password: Minimum 8 characters (enforced by backend, validated on frontend)

**State Transitions**: User goes from `null` (unauthenticated) → `User` object (authenticated) → `null` (logged out)

---

### Task

Represents a todo task owned by a user.

```typescript
// types/task.types.ts

export enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

export interface Task {
  id: string;                          // UUID as string
  user_id: string;                     // Owner's user ID (UUID)
  title: string;                       // Task title (1-255 chars)
  description: string;                 // Optional description
  status: TaskStatus;                  // Task status
  priority: TaskPriority;              // Task priority
  due_date: string | null;             // ISO 8601 timestamp or null
  completed_at: string | null;         // ISO 8601 timestamp or null
  is_deleted: boolean;                 // Soft delete flag
  created_at: string;                  // ISO 8601 timestamp
  updated_at: string;                  // ISO 8601 timestamp
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: TaskStatus;                 // Defaults to PENDING
  priority?: TaskPriority;             // Defaults to MEDIUM
  due_date?: string | null;            // ISO 8601 timestamp
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string | null;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;                       // Total count (for pagination)
  page: number;                        // Current page
  page_size: number;                   // Items per page
}

export interface TaskFilters {
  status?: TaskStatus;
  priority?: TaskPriority;
  due_before?: string;                 // ISO 8601 timestamp
  page?: number;
  page_size?: number;
}
```

**Validation Rules**:
- Title: Required, 1-255 characters
- Description: Optional, max 1000 characters
- Status: Must be one of TaskStatus enum values
- Priority: Must be one of TaskPriority enum values
- Due Date: Must be valid ISO 8601 timestamp or null

**State Transitions**:
```
PENDING → IN_PROGRESS → COMPLETED
   ↓           ↓             ↓
DELETED (soft delete, is_deleted = true)
```

---

### ChatMessage

Represents a message in the chatbot conversation.

```typescript
// types/chat.types.ts

export enum ChatIntent {
  CREATE_TASK = 'create_task',
  LIST_TASKS = 'list_tasks',
  UPDATE_TASK = 'update_task',
  COMPLETE_TASK = 'complete_task',
  DELETE_TASK = 'delete_task',
  SET_REMINDER = 'set_reminder',
  HELP = 'help',
  UNKNOWN = 'unknown',
}

export enum MessageSender {
  USER = 'user',
  BOT = 'bot',
}

export interface ChatMessage {
  id: string;                          // Client-generated UUID
  sender: MessageSender;               // 'user' or 'bot'
  content: string;                     // Message text
  timestamp: Date;                     // When message was sent
  intent?: ChatIntent;                 // Detected intent (bot messages only)
  data?: Record<string, any>;          // Additional data (e.g., task info)
  clarification_needed?: boolean;      // Whether bot needs clarification
  clarification_questions?: string[];  // Follow-up questions
  action_taken?: string;               // Description of action (e.g., "Task created")
}

export interface ChatRequest {
  message: string;                     // User's message (1-1000 chars)
  context?: Record<string, any>;       // Optional conversation context
}

export interface ChatResponse {
  response: string;                    // Bot's response text
  intent: ChatIntent;                  // Detected intent
  clarification_needed: boolean;       // Whether clarification needed
  clarification_questions?: string[];  // Questions for user
  action_taken?: string;               // Action description
  data?: Record<string, any>;          // Additional data (e.g., created task)
}
```

**Validation Rules**:
- Message content: Required, 1-1000 characters
- Sender: Must be 'user' or 'bot'

**State Flow**:
```
1. User types message → ChatMessage (sender: USER, content: "...")
2. Frontend sends ChatRequest to backend
3. Backend responds with ChatResponse
4. Frontend creates ChatMessage (sender: BOT, content: response.response, intent: response.intent)
5. Both messages added to chat history (React state)
```

---

## Component State Types

### Auth State (Global Context)

```typescript
// contexts/AuthContext.tsx

export interface AuthContextType {
  user: User | null;                   // Current user or null if not authenticated
  loading: boolean;                    // Whether auth state is loading
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<boolean>; // Returns true if refresh succeeded
}
```

**Storage**:
- Tokens stored in `localStorage` under keys:
  - `access_token`: JWT access token
  - `refresh_token`: JWT refresh token
- User object stored in React Context state (in-memory)

**Lifecycle**:
```
1. App mounts → AuthProvider checks localStorage for tokens
2. If tokens exist → Verify token with backend → Set user state
3. If tokens invalid/expired → Attempt refresh → If refresh fails → Clear state and redirect to login
4. User logs in → Store tokens in localStorage → Set user state
5. User logs out → Clear tokens from localStorage → Clear user state → Redirect to login
```

---

### Chat State (Component-Scoped)

```typescript
// components/chat/ChatInterface.tsx

interface ChatState {
  messages: ChatMessage[];             // Chat history (in-memory, not persisted)
  input: string;                       // Current input field value
  isTyping: boolean;                   // Whether bot is "typing" (API call in progress)
  error: string | null;                // Error message to display
}
```

**Lifecycle**:
```
1. ChatInterface mounts → Initialize empty messages array
2. User types → Update input state
3. User sends → Add user message to messages → Clear input → Set isTyping = true
4. API call completes → Add bot message to messages → Set isTyping = false
5. API call fails → Set error state → Set isTyping = false
6. Page refresh → Chat history lost (not persisted)
```

---

### Task List State (Optional Caching)

```typescript
// hooks/useTasks.ts

interface TaskState {
  tasks: Task[];                       // Cached task list
  total: number;                       // Total count
  page: number;                        // Current page
  page_size: number;                   // Items per page
  loading: boolean;                    // Whether tasks are loading
  error: string | null;                // Error message
  filters: TaskFilters;                // Active filters
}
```

**Caching Strategy** (optional, future enhancement):
- Use React Query or SWR for client-side caching
- Cache invalidation on task create/update/delete
- Stale-while-revalidate pattern (show cached data, fetch fresh in background)

**Current Implementation** (MVP):
- No caching, fetch tasks on demand via chatbot responses
- Tasks displayed in bot messages only (no separate task list view yet)

---

## Local Storage Schema

Frontend stores JWT tokens and optionally cached data in browser localStorage.

```typescript
// lib/token.ts

export interface LocalStorageSchema {
  access_token: string | null;         // JWT access token
  refresh_token: string | null;        // JWT refresh token
  // Future: chat_history, user_preferences, etc.
}
```

**Keys**:
- `access_token` - JWT access token (string)
- `refresh_token` - JWT refresh token (string)

**Security Notes**:
- localStorage is vulnerable to XSS attacks
- Tokens have short expiry (1 hour for access, 7 days for refresh)
- Implement Content Security Policy (CSP) to mitigate XSS
- Future: Consider httpOnly cookies if backend supports

---

## API Response Error Handling

```typescript
// types/api.types.ts

export interface APIError {
  status: number;                      // HTTP status code
  message: string;                     // Error message from backend
  detail?: string;                     // Additional error details
}

export interface FieldError {
  field: string;                       // Field name (e.g., "email")
  message: string;                     // Error message (e.g., "Invalid email")
}

export interface ValidationError extends APIError {
  status: 422;                         // Unprocessable Entity
  errors: FieldError[];                // List of field-specific errors
}
```

**Error Handling Pattern**:
```typescript
try {
  const response = await api.post('/api/chat/message', { message });
  // Success
} catch (error) {
  if (error.response?.status === 401) {
    // Unauthorized - attempt token refresh
  } else if (error.response?.status === 422) {
    // Validation error - display field errors
  } else if (error.response?.status >= 500) {
    // Server error - display generic error message
  } else {
    // Network error - display "Check your connection"
  }
}
```

---

## Type Utilities

```typescript
// types/utils.ts

// Convert API date strings to Date objects
export type WithDates<T> = {
  [K in keyof T]: T[K] extends string
    ? K extends `${string}_at` | 'due_date'
      ? Date | null
      : T[K]
    : T[K];
};

// Example: Convert Task with ISO strings to Task with Date objects
export type TaskWithDates = WithDates<Task>;

// Utility to convert API response to typed object with Date conversion
export function parseAPIDates<T>(obj: T): WithDates<T> {
  const result = { ...obj } as any;
  for (const key in result) {
    if (key.endsWith('_at') || key === 'due_date') {
      if (typeof result[key] === 'string') {
        result[key] = parseISO(result[key]); // date-fns
      }
    }
  }
  return result;
}
```

---

## Summary

### Entity Types
- **User**: Authentication and user profile
- **Task**: Todo tasks with status, priority, due date
- **ChatMessage**: Conversation messages with sender, intent, metadata

### State Types
- **AuthContext**: Global auth state (user, login, logout)
- **ChatState**: Component-scoped chat history and input
- **TaskState**: Optional task list caching (future enhancement)

### Storage
- **localStorage**: JWT tokens (access_token, refresh_token)
- **React Context**: User object (in-memory)
- **Component State**: Chat messages (in-memory, session-scoped)

### Type Safety
- All API calls typed with request/response interfaces
- Enum types for status, priority, intent (prevents typos)
- Utility types for date conversion (ISO strings → Date objects)

**Next Steps**: Generate API contracts (OpenAPI) and create TypeScript types from contracts
