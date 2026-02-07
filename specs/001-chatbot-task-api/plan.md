# Implementation Plan: AI-Powered Todo Chatbot Backend API

**Branch**: `001-chatbot-task-api` | **Date**: 2025-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-chatbot-task-api/spec.md`

## Summary

Implement a backend API that enables an AI chatbot to manage tasks via natural language commands. The solution extends the existing FastAPI backend with:
1. Enhanced task model (priority, due_date, completed_at)
2. Task reminder system
3. Chatbot integration endpoint for NLP-processed commands
4. Complete task completion endpoint (PATCH)

The existing codebase already has JWT authentication, user isolation, and basic task CRUD. This plan builds on that foundation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, SQLModel, python-jose, passlib, openai-agents-sdk
**Storage**: Neon Serverless PostgreSQL (existing)
**Testing**: pytest with pytest-asyncio
**Target Platform**: Linux server (Docker-compatible)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: API <500ms p95, Chatbot <2s including NLP
**Constraints**: 100 concurrent users, user isolation mandatory
**Scale/Scope**: Multi-tenant SaaS, task-per-user isolation

## Constitution Check

*GATE: Must pass before implementation. All principles verified against plan.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. User Data Isolation | ✅ PASS | All queries filter by `user_id` from JWT; existing pattern maintained |
| II. AI-First Interaction | ✅ PASS | Chatbot endpoint processes NLP commands via OpenAI Agents SDK |
| III. API-Driven Architecture | ✅ PASS | REST endpoints for all operations; chatbot uses same API |
| IV. Test-Driven Development | ✅ PASS | Contract tests for new endpoints; integration tests for auth |
| V. Performance & Responsiveness | ✅ PASS | Indexes on user_id, due_date; connection pooling configured |
| VI. Secure Authentication | ✅ PASS | JWT required on all endpoints; 1-hour expiry; bcrypt passwords |

## Project Structure

### Documentation (this feature)

```text
specs/001-chatbot-task-api/
├── spec.md              # Feature specification
├── plan.md              # This file
├── data-model.md        # Entity definitions and relationships
├── contracts/           # API endpoint contracts
│   ├── tasks.yaml       # Task CRUD endpoints
│   ├── reminders.yaml   # Reminder endpoints
│   └── chatbot.yaml     # Chatbot integration endpoint
└── checklists/
    └── requirements.md  # Quality validation checklist
```

### Source Code (repository root)

```text
backend/
├── main.py                      # FastAPI application (existing)
├── core/
│   ├── config.py                # Configuration (existing)
│   ├── db.py                    # Database connection (existing)
│   └── security.py              # JWT handling (existing)
├── models/
│   ├── task.py                  # Task model (MODIFY: add priority, due_date, completed_at)
│   ├── user.py                  # User model (existing)
│   └── reminder.py              # NEW: TaskReminder model
├── routes/
│   ├── tasks.py                 # Task endpoints (MODIFY: add complete, filter endpoints)
│   ├── reminders.py             # NEW: Reminder endpoints
│   └── chatbot.py               # NEW: Chatbot integration endpoint
├── schemas/
│   ├── task.py                  # Task schemas (MODIFY: add new fields)
│   ├── reminder.py              # NEW: Reminder schemas
│   └── chatbot.py               # NEW: Chatbot request/response schemas
├── services/
│   ├── task_service.py          # Task service (MODIFY: add filter methods)
│   ├── reminder_service.py      # NEW: Reminder service
│   └── chatbot_service.py       # NEW: Chatbot command processor
└── tests/
    ├── test_tasks.py            # Task endpoint tests (MODIFY: add new tests)
    ├── test_reminders.py        # NEW: Reminder endpoint tests
    └── test_chatbot.py          # NEW: Chatbot endpoint tests

frontend/
├── src/
│   ├── components/
│   │   └── chatbot/             # NEW: Chatbot widget components
│   │       ├── ChatWidget.tsx
│   │       ├── MessageBubble.tsx
│   │       └── QuickReplies.tsx
│   └── services/
│       └── chatbot.ts           # NEW: Chatbot API service
└── tests/
    └── chatbot.test.tsx         # NEW: Chatbot component tests
```

**Structure Decision**: Using existing web application structure (backend/ + frontend/). Extending existing patterns for models, routes, and services.

## Architecture Decisions

### AD-001: Extend Existing Task Model vs. New Model

**Decision**: Extend existing Task model with new fields (priority, due_date, completed_at)

**Rationale**:
- Existing model already has user_id isolation
- Migration is simpler than creating new model
- Maintains backward compatibility with existing frontend

**Alternatives Rejected**:
- New TaskV2 model: Would require migrating existing data and updating all references

### AD-002: Chatbot Endpoint Architecture

**Decision**: Single `/api/chat/message` endpoint that processes NLP commands and routes to existing task services

**Rationale**:
- Chatbot layer translates natural language to structured API calls
- Reuses existing task service logic
- Maintains separation between NLP processing and business logic

**Implementation**:
```
User Message → /api/chat/message → ChatbotService
                                         ↓
                              OpenAI Agents SDK (intent/entity extraction)
                                         ↓
                              Route to TaskService/ReminderService
                                         ↓
                              Structured Response → User
```

### AD-003: Reminder Storage Strategy

**Decision**: Store reminders in separate `task_reminders` table linked to tasks

**Rationale**:
- One task can have multiple reminders
- Allows independent reminder processing
- Clean separation of concerns

### AD-004: Task Status Values

**Decision**: Expand status from `pending|completed` to `pending|in_progress|completed`

**Rationale**:
- More granular task tracking
- Aligns with spec requirement
- Backward compatible (existing tasks remain valid)

## API Contracts

### Task Endpoints (Enhanced)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/tasks` | List user's tasks (with filters) | JWT |
| POST | `/api/tasks` | Create task | JWT |
| GET | `/api/tasks/{id}` | Get single task | JWT |
| PUT | `/api/tasks/{id}` | Update task | JWT |
| DELETE | `/api/tasks/{id}` | Delete task | JWT |
| PATCH | `/api/tasks/{id}/complete` | Mark task complete | JWT |

### Reminder Endpoints (New)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/tasks/{id}/reminders` | Create reminder for task | JWT |
| GET | `/api/tasks/{id}/reminders` | List reminders for task | JWT |
| DELETE | `/api/reminders/{id}` | Delete reminder | JWT |

### Chatbot Endpoint (New)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/chat/message` | Process chatbot message | JWT |

## Data Model Changes

### Task Model (Modified)

```python
class Task(SQLModel, table=True):
    id: UUID
    user_id: str                    # Existing
    title: str                      # Existing
    description: Optional[str]      # Existing
    status: str                     # Modified: pending|in_progress|completed
    priority: str                   # NEW: low|medium|high|urgent (default: medium)
    due_date: Optional[datetime]    # NEW
    completed_at: Optional[datetime] # NEW
    created_at: datetime            # Existing
    updated_at: datetime            # Existing
    is_deleted: bool                # NEW: soft delete support
```

### TaskReminder Model (New)

```python
class TaskReminder(SQLModel, table=True):
    id: UUID
    task_id: UUID                   # FK to Task
    user_id: str                    # For user isolation
    remind_at: datetime             # When to send reminder
    is_sent: bool                   # Default: False
    sent_at: Optional[datetime]     # When reminder was sent
    created_at: datetime
```

## Implementation Phases

### Phase 1: Data Model Updates (Foundation)
- Extend Task model with priority, due_date, completed_at, is_deleted
- Create TaskReminder model
- Database migration for new fields
- Update schemas for new fields

### Phase 2: Task API Enhancements
- Add PATCH `/api/tasks/{id}/complete` endpoint
- Add filtering to GET `/api/tasks` (status, priority, due_date)
- Update TaskService with filter methods
- Add soft delete support

### Phase 3: Reminder System
- Create ReminderService
- Add reminder CRUD endpoints
- Link reminders to tasks

### Phase 4: Chatbot Integration
- Create ChatbotService with OpenAI Agents SDK
- Define intents and entity extraction
- Implement `/api/chat/message` endpoint
- Create chatbot response formatting

### Phase 5: Frontend Chatbot Widget
- Create ChatWidget component
- Implement message handling
- Add quick reply buttons
- Integrate with chatbot API

### Phase 6: Testing & Polish
- Contract tests for all new endpoints
- Integration tests for chatbot flow
- Performance testing
- Documentation updates

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| OpenAI API latency | Set 5s timeout; cache common intents; fallback to pattern matching |
| Database migration issues | Use Alembic with reversible migrations; test on staging first |
| Chatbot misinterpretation | Implement clarification prompts; log unrecognized intents for improvement |
| Reminder processing delays | Use background task queue; monitor delivery latency |

## Complexity Tracking

No constitution violations identified. Plan stays within established patterns:
- Single backend/frontend structure ✅
- Extends existing models rather than creating parallel systems ✅
- Reuses existing auth and service patterns ✅

## Dependencies

### External Dependencies
- `openai` - OpenAI Agents SDK for NLP
- `apscheduler` - Background job scheduling for reminders (optional)

### Internal Dependencies
- Existing JWT authentication (core/security.py)
- Existing database session management (core/db.py)
- Existing task service patterns (services/task_service.py)

## Success Metrics Alignment

| Success Criterion | Implementation Approach |
|------------------|------------------------|
| SC-001: Task creation <5s | Direct DB insert; no external calls |
| SC-002: Task viewing <2s | Indexed queries; pagination |
| SC-003: 100% user isolation | All queries filter by JWT user_id |
| SC-004: 100 concurrent users | Connection pooling; async endpoints |
| SC-005: 95% NLP accuracy | OpenAI fine-tuning; fallback patterns |
| SC-006: Reminders <1min accuracy | Background scheduler with 30s intervals |
| SC-007: Chatbot-friendly errors | Structured error responses with suggestions |
| SC-008: Auth failures <1s | JWT validation is synchronous |
