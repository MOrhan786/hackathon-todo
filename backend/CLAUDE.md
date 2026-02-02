# Claude Code Instructions: Phase II Backend API

## Project Context
This is the backend for Hackathon II - Phase II of the Todo Application. It implements a secure task management API using FastAPI, SQLModel ORM, and Neon PostgreSQL with JWT-based authentication and user isolation.

## Architecture
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT-based with independent verification
- **Security**: User isolation enforcement at API and database levels

## Folder Structure
```
backend/
├── main.py              # FastAPI application entry point
├── core/
│   ├── db.py            # Database connection and session management
│   ├── config.py        # Configuration and environment variables
│   └── security.py      # JWT handling and security utilities
├── models/
│   └── task.py          # SQLModel definitions for tasks and user relationships
├── routes/
│   └── tasks.py         # Task-related API endpoints
├── schemas/             # Pydantic models for request/response validation
├── utils/               # Utility functions
└── CLAUDE.md            # Claude Code instructions for backend
```

## Key Requirements
1. All API endpoints must require JWT authentication
2. Backend must verify JWT tokens independently using shared secret
3. Users must only access tasks associated with their user ID
4. Proper input validation using schemas
5. Consistent error responses with appropriate HTTP status codes
6. Database operations must use connection pooling
7. Proper error handling and logging

## Security Rules
- Never trust user_id from request body or URL alone
- Always extract user identity from JWT token
- Always filter database queries by authenticated user
- Return 401 for unauthorized requests
- Return 403 for unauthorized access attempts to other users' data

## Quality Standards
- Clean, readable code with proper separation of concerns
- Input validation on all endpoints
- Consistent error response format
- Environment-based configuration
- No hard-coded secrets