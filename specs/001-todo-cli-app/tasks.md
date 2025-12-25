# Implementation Tasks: Todo In-Memory Python Console App

**Feature**: Todo In-Memory Python Console App
**Branch**: `001-todo-cli-app`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)
**Status**: Ready for implementation

## Implementation Strategy

This task list implements the Todo In-Memory Python Console App following a phased approach:

1. **MVP First**: Complete User Story 1 (Add New Tasks) first to establish core functionality
2. **Incremental Delivery**: Each user story builds on the previous to create a complete, independently testable increment
3. **Parallel Opportunities**: Identified where tasks can be worked on in parallel (marked with [P])
4. **Manual Validation**: After each phase, validate functionality with `uv run todo` commands

## Dependencies

User stories follow this dependency order:
- US1 (Add Tasks) → US2 (View Tasks) → US3 (Update Tasks) → US4 (Complete Tasks) → US5 (Delete Tasks)

## Parallel Execution Examples

- T003 [P], T004 [P], T005 [P]: Core models and storage components can be developed in parallel
- T012 [P], T013 [P], T014 [P], T015 [P]: CLI commands can be developed in parallel after core components are complete

---

## Phase 1: Setup Tasks

**Goal**: Initialize project structure and foundational components

- [X] T001 Create src/todo directory structure
- [X] T002 Create basic __init__.py file in src/todo/

## Phase 2: Foundational Tasks

**Goal**: Implement core models and storage layer - blocking prerequisite for all user stories

- [X] T003 [P] Create models.py with Task dataclass (id, title, description, completed, created_at)
- [X] T004 [P] Create storage.py with InMemoryTaskStorage class
- [X] T005 [P] Implement empty task list and next_id counter in storage.py
- [X] T006 Implement add_task function in storage.py (auto-increment ID, timestamp)
- [X] T007 Implement get_all_tasks function in storage.py
- [X] T008 Implement get_task_by_id function in storage.py with error handling
- [X] T009 Implement update_task function in storage.py (optional title/desc changes)
- [X] T010 Implement delete_task function in storage.py
- [X] T011 Implement toggle_task_status function in storage.py

## Phase 3: User Story 1 - Add New Tasks (Priority: P1)

**Goal**: As a user, I want to add new tasks to my todo list so that I can keep track of things I need to do.

**Independent Test**: The application can be fully tested by adding tasks with titles and descriptions, and these tasks are stored in memory and can be viewed later.

- [X] T012 [P] [US1] Create cli.py with TodoCLI class structure
- [X] T013 [P] [US1] Implement add_task method in cli.py (parse title/desc, call storage.add_task, print success)
- [X] T014 [P] [US1] Add argparse setup for add command in cli.py
- [X] T015 [P] [US1] Implement run method in cli.py to handle add command
- [X] T016 [US1] Test add functionality with manual validation: uv run src/todo/__main__.py add --title "Test" --description "Test desc"

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: As a user, I want to view all my tasks in a clear, tabular format so that I can see what I need to do and track my progress.

**Independent Test**: The application can be tested by displaying all tasks in a tabular format with clear status indicators ([ ] for pending, [x] for completed).

- [X] T017 [P] [US2] Implement list_tasks method in cli.py (format tabular output with [ ]/[x], truncate desc, handle empty)
- [X] T018 [P] [US2] Add argparse setup for list command in cli.py
- [X] T019 [P] [US2] Update run method in cli.py to handle list command
- [X] T020 [US2] Test list functionality with manual validation: uv run src/todo/__main__.py list

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: As a user, I want to update task details by ID so that I can modify information about tasks without deleting and recreating them.

**Independent Test**: The application can be tested by updating specific task details (title or description) by referencing its ID, and the changes are reflected when viewing the task again.

- [X] T021 [P] [US3] Implement update_task method in cli.py (parse ID and optional changes, call storage.update_task)
- [X] T022 [P] [US3] Add argparse setup for update command in cli.py
- [X] T023 [P] [US3] Update run method in cli.py to handle update command
- [X] T024 [US3] Test update functionality with manual validation: uv run src/todo/__main__.py update --id 1 --title "Updated"

## Phase 6: User Story 4 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: As a user, I want to mark tasks as complete or incomplete so that I can track my progress and organize my work.

**Independent Test**: The application can be tested by toggling the status of tasks between complete and incomplete, with the status indicators updating accordingly in the display.

- [X] T025 [P] [US4] Implement complete_task method in cli.py (parse ID, call storage.toggle_task_status)
- [X] T026 [P] [US4] Add argparse setup for complete command in cli.py
- [X] T027 [P] [US4] Update run method in cli.py to handle complete command
- [X] T028 [US4] Test complete functionality with manual validation: uv run src/todo/__main__.py complete --id 1

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: As a user, I want to delete tasks I no longer need so that I can keep my todo list clean and focused.

**Independent Test**: The application can be tested by deleting specific tasks by ID and confirming they no longer appear in the task list.

- [X] T029 [P] [US5] Implement delete_task method in cli.py (parse ID, call storage.delete_task)
- [X] T030 [P] [US5] Add argparse setup for delete command in cli.py
- [X] T031 [P] [US5] Update run method in cli.py to handle delete command
- [X] T032 [US5] Test delete functionality with manual validation: uv run src/todo/__main__.py delete --id 1

## Phase 8: Entry Point & Integration

**Goal**: Complete the application by adding the entry point and testing full integration

- [X] T033 Create __main__.py to run cli.main()
- [X] T034 Test full integration with uv run todo commands
- [X] T035 Add input validation and sanitization to prevent injection attacks (FR-012)

## Phase 9: Documentation & Demo Prep

**Goal**: Prepare documentation and validate complete functionality

- [X] T036 Update README.md with project overview, setup (uv venv & sync), usage examples (uv run todo ...)
- [X] T037 Add sample demo commands and expected outputs to README.md
- [X] T038 Final validation: Run full workflow, ensure all features work with edge cases
- [X] T039 Verify all functional requirements (FR-001 through FR-012) are met
- [X] T040 Verify all success criteria (SC-001 through SC-007) are met