# Tasks: AI-Powered Todo Chatbot Backend API

**Input**: Design documents from `/specs/001-chatbot-task-api/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Tests**: Tests are included based on Constitution Principle IV (Test-Driven Development).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` for Python API, `frontend/` for Next.js
- Existing files: models/task.py, routes/tasks.py, services/task_service.py, schemas/task.py

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install new dependencies and prepare project structure

- [ ] T001 Add openai package to backend/requirements.txt for OpenAI Agents SDK
- [ ] T002 [P] Create backend/models/reminder.py file (empty placeholder)
- [ ] T003 [P] Create backend/routes/reminders.py file (empty placeholder)
- [ ] T004 [P] Create backend/routes/chatbot.py file (empty placeholder)
- [ ] T005 [P] Create backend/services/reminder_service.py file (empty placeholder)
- [ ] T006 [P] Create backend/services/chatbot_service.py file (empty placeholder)
- [ ] T007 [P] Create backend/schemas/reminder.py file (empty placeholder)
- [ ] T008 [P] Create backend/schemas/chatbot.py file (empty placeholder)
- [ ] T009 [P] Create backend/tests/ directory structure if not exists

**Checkpoint**: All new files created, dependencies added

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data model updates and core infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 Add TaskStatus enum (pending/in_progress/completed) to backend/models/task.py
- [ ] T011 Add TaskPriority enum (low/medium/high/urgent) to backend/models/task.py
- [ ] T012 Add priority field to Task model in backend/models/task.py (default: medium)
- [ ] T013 Add due_date field (Optional[datetime]) to Task model in backend/models/task.py
- [ ] T014 Add completed_at field (Optional[datetime]) to Task model in backend/models/task.py
- [ ] T015 Add is_deleted field (bool, default=False) to Task model in backend/models/task.py
- [ ] T016 Update TaskCreate schema with priority and due_date in backend/schemas/task.py
- [ ] T017 Update TaskUpdate schema with priority and due_date in backend/schemas/task.py
- [ ] T018 Update TaskResponse schema with new fields in backend/schemas/task.py
- [ ] T019 Create TaskReminder model in backend/models/reminder.py per data-model.md
- [ ] T020 Create ReminderCreate schema in backend/schemas/reminder.py
- [ ] T021 Create ReminderResponse schema in backend/schemas/reminder.py
- [ ] T022 Create ReminderListResponse schema in backend/schemas/reminder.py
- [ ] T023 Update backend/models/__init__.py to export new models
- [ ] T024 Run database migration to add new columns to tasks table
- [ ] T025 Run database migration to create task_reminders table

**Checkpoint**: Foundation ready - all models and schemas updated, database migrated

---

## Phase 3: User Story 7 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Ensure JWT authentication is working for all chatbot operations

**Independent Test**: Attempt to access task endpoints without a token and verify rejection

**Note**: Authentication already exists in the codebase. This phase verifies and extends it.

### Implementation for User Story 7

- [ ] T026 [US7] Verify JWT token expiry is set to 1 hour in backend/core/config.py
- [ ] T027 [US7] Verify get_current_user dependency extracts user_id from JWT in backend/core/security.py
- [ ] T028 [US7] Add refresh token endpoint to backend/src/api/auth.py if not exists
- [ ] T029 [US7] Create test_auth.py in backend/tests/ to verify authentication flow

**Checkpoint**: Authentication verified and working

---

## Phase 4: User Story 1 - Create Task via Chatbot (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by sending natural language commands to the chatbot

**Independent Test**: Send "Create a task called Buy groceries due tomorrow" and verify task appears in list

### Implementation for User Story 1

- [ ] T030 [US1] Add filter parameters (status, priority, due_before) to GET /api/tasks in backend/routes/tasks.py
- [ ] T031 [US1] Implement get_tasks_filtered method in backend/services/task_service.py
- [ ] T032 [US1] Create ChatRequest schema in backend/schemas/chatbot.py
- [ ] T033 [US1] Create ChatResponse schema in backend/schemas/chatbot.py
- [ ] T034 [US1] Create intent extraction logic using OpenAI in backend/services/chatbot_service.py
- [ ] T035 [US1] Implement create_task intent handler in backend/services/chatbot_service.py
- [ ] T036 [US1] Create POST /api/chat/message endpoint in backend/routes/chatbot.py
- [ ] T037 [US1] Register chatbot router in backend/main.py
- [ ] T038 [US1] Add validation for task title (non-empty, max 255 chars) in chatbot service
- [ ] T039 [US1] Add clarification prompt when task title is missing in chatbot response

**Checkpoint**: Can create tasks via chatbot - "Add task: Buy groceries" works

---

## Phase 5: User Story 2 - View Tasks via Chatbot (Priority: P1) 🎯 MVP

**Goal**: Users can ask the chatbot to show their tasks with optional filters

**Independent Test**: Ask "Show my tasks" and verify chatbot returns user's tasks

### Implementation for User Story 2

- [ ] T040 [US2] Implement list_tasks intent handler in backend/services/chatbot_service.py
- [ ] T041 [US2] Add filter parsing for "due today", "completed", "pending" in chatbot service
- [ ] T042 [US2] Format task list response for chatbot display in backend/services/chatbot_service.py
- [ ] T043 [US2] Handle empty task list response with helpful message
- [ ] T044 [US2] Add pagination support for large task lists (default 20)

**Checkpoint**: Can view tasks via chatbot - "Show my tasks" works

---

## Phase 6: User Story 3 - Update Task via Chatbot (Priority: P2)

**Goal**: Users can update task details through natural language commands

**Independent Test**: Say "Change task priority to high" and verify task is updated

### Implementation for User Story 3

- [ ] T045 [US3] Implement update_task intent handler in backend/services/chatbot_service.py
- [ ] T046 [US3] Add task reference resolution (by title, by position) in chatbot service
- [ ] T047 [US3] Parse update fields (title, priority, due_date, description) from natural language
- [ ] T048 [US3] Add "task not found" response handling
- [ ] T049 [US3] Add confirmation response for successful updates

**Checkpoint**: Can update tasks via chatbot - "Update Buy groceries to due Friday" works

---

## Phase 7: User Story 4 - Complete Task via Chatbot (Priority: P2)

**Goal**: Users can mark tasks as complete using the chatbot

**Independent Test**: Say "Complete task Buy groceries" and verify task status is "completed"

### Implementation for User Story 4

- [ ] T050 [US4] Create PATCH /api/tasks/{id}/complete endpoint in backend/routes/tasks.py
- [ ] T051 [US4] Implement complete_task method in backend/services/task_service.py (sets completed_at)
- [ ] T052 [US4] Implement complete_task intent handler in backend/services/chatbot_service.py
- [ ] T053 [US4] Handle "already completed" case with appropriate response
- [ ] T054 [US4] Add completion confirmation message with task title

**Checkpoint**: Can complete tasks via chatbot - "Mark Buy groceries as done" works

---

## Phase 8: User Story 5 - Delete Task via Chatbot (Priority: P2)

**Goal**: Users can delete tasks through the chatbot

**Independent Test**: Say "Delete task Buy groceries" and verify task is soft-deleted

### Implementation for User Story 5

- [ ] T055 [US5] Update DELETE /api/tasks/{id} to use soft delete (set is_deleted=True) in backend/routes/tasks.py
- [ ] T056 [US5] Update get_tasks_by_user to filter out is_deleted=True in backend/services/task_service.py
- [ ] T057 [US5] Implement delete_task intent handler in backend/services/chatbot_service.py
- [ ] T058 [US5] Add deletion confirmation message
- [ ] T059 [US5] Handle "task not found" for delete attempts

**Checkpoint**: Can delete tasks via chatbot - "Delete Buy groceries task" works

---

## Phase 9: User Story 6 - Set Task Reminder (Priority: P3)

**Goal**: Users can set reminders for tasks through the chatbot

**Independent Test**: Say "Remind me about Buy groceries in 1 hour" and verify reminder is created

### Implementation for User Story 6

- [ ] T060 [US6] Implement ReminderService in backend/services/reminder_service.py
- [ ] T061 [US6] Create POST /api/tasks/{id}/reminders endpoint in backend/routes/reminders.py
- [ ] T062 [US6] Create GET /api/tasks/{id}/reminders endpoint in backend/routes/reminders.py
- [ ] T063 [US6] Create DELETE /api/reminders/{id} endpoint in backend/routes/reminders.py
- [ ] T064 [US6] Register reminders router in backend/main.py
- [ ] T065 [US6] Implement set_reminder intent handler in backend/services/chatbot_service.py
- [ ] T066 [US6] Parse relative time expressions ("in 1 hour", "tomorrow at 9am") in chatbot service
- [ ] T067 [US6] Add reminder confirmation message with scheduled time

**Checkpoint**: Can set reminders via chatbot - "Remind me about Buy groceries tomorrow at 9am" works

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Quality improvements, testing, and documentation

- [ ] T068 [P] Add help intent handler with list of available commands in backend/services/chatbot_service.py
- [ ] T069 [P] Add unknown intent fallback with suggestions in chatbot service
- [ ] T070 [P] Create contract tests for task endpoints in backend/tests/test_tasks.py
- [ ] T071 [P] Create contract tests for reminder endpoints in backend/tests/test_reminders.py
- [ ] T072 [P] Create integration tests for chatbot flow in backend/tests/test_chatbot.py
- [ ] T073 Add structured error responses with suggestions field for chatbot-friendly errors
- [ ] T074 Add request logging for chatbot messages in backend/routes/chatbot.py
- [ ] T075 Update API documentation in backend/README.md with new endpoints
- [ ] T076 Verify user isolation: all queries filter by authenticated user_id
- [ ] T077 Performance check: verify API response times meet <500ms p95 target

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phase 3 (US7 Auth)**: Depends on Phase 2
- **Phases 4-9 (User Stories)**: Depend on Phase 2 and Phase 3
- **Phase 10 (Polish)**: Depends on all user stories

### User Story Dependencies

- **US7 (Auth)**: Foundation only - can start after Phase 2
- **US1 (Create)**: Depends on US7 - first chatbot functionality
- **US2 (View)**: Can run parallel with US1 after US7
- **US3 (Update)**: Depends on US1/US2 (need tasks to update)
- **US4 (Complete)**: Depends on US1 (need tasks to complete)
- **US5 (Delete)**: Depends on US1 (need tasks to delete)
- **US6 (Reminders)**: Depends on US1 (need tasks for reminders)

### Parallel Opportunities

**Phase 1 (all parallel)**:
```
T002, T003, T004, T005, T006, T007, T008, T009
```

**Phase 2 (sequential for model changes)**:
```
T010 → T011 → T012 → T013 → T014 → T015 (same file)
T016, T017, T018 (parallel - different files)
T019 → T020 → T021 → T022 (reminder models)
```

**User Stories (can be parallel after Phase 3)**:
```
US1 + US2 can run in parallel
US3, US4, US5, US6 can run in parallel after US1/US2
```

---

## Implementation Strategy

### MVP First (Phases 1-5)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: Authentication verification
4. Complete Phase 4: Create Task (US1)
5. Complete Phase 5: View Tasks (US2)
6. **STOP and VALIDATE**: Test create + view via chatbot
7. Deploy/demo MVP

### Incremental Delivery

| Increment | Stories | Value Delivered |
|-----------|---------|-----------------|
| MVP | US1 + US2 | Create and view tasks via chatbot |
| +Update | US3 + US4 | Modify and complete tasks |
| +Delete | US5 | Remove unwanted tasks |
| +Reminders | US6 | Schedule task reminders |

### Suggested MVP Scope

**Minimum**: Phase 1 + 2 + 3 + 4 + 5 (T001-T044)
- Users can create tasks via chatbot
- Users can view their tasks via chatbot
- Full authentication in place

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Existing code patterns in backend/ should be followed
- All chatbot intents route through ChatbotService to TaskService
- User isolation enforced via get_current_user dependency on all endpoints
- Soft delete preferred over hard delete for undo capability
