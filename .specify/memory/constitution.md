<!--
  ============================================================================
  SYNC IMPACT REPORT
  ============================================================================
  Version Change: 1.0.0 → 2.0.0

  Added Principles:
    - VII. Intelligent Task Organization (NEW)
    - VIII. Event-Driven Architecture (NEW)
    - IX. Distributed Application Runtime (NEW)
    - X. Cloud-Native Deployment (NEW)

  Modified Principles:
    - II. AI-First Interaction (EXPANDED - recurring tasks, reminders via chatbot)
    - V. Performance & Responsiveness (EXPANDED - event-driven, Kafka latency)

  Added Sections:
    - Phase V Technology Stack additions (Kafka, Dapr, DOKS)
    - Feature Levels (Intermediate + Advanced)

  Removed Sections: None

  Templates Requiring Updates:
    ✅ plan-template.md - Constitution Check section compatible
    ✅ spec-template.md - Requirements structure compatible
    ✅ tasks-template.md - Phase structure compatible

  Deferred Items: None
  ============================================================================
-->

# AI Chatbot Todo App Constitution

## Core Principles

### I. User Data Isolation

Every user MUST interact only with their own tasks and data. User isolation is non-negotiable.

**Rules**:
- All database queries MUST filter by authenticated user ID
- API endpoints MUST validate user ownership before any CRUD operation
- Chatbot responses MUST never expose or reference other users' data
- Session context MUST be scoped to the authenticated user
- Event messages MUST include user_id for consumer-side isolation

**Rationale**: User privacy and data security are foundational to trust. A multi-tenant task system without strict isolation is a security vulnerability.

### II. AI-First Interaction

The chatbot is the primary interface for task management. Natural language processing MUST provide intuitive task operations including advanced features.

**Rules**:
- Chatbot MUST support Create, View, Update, Delete, Search, Filter, and Sort operations via natural language
- Chatbot MUST handle recurring task setup (e.g., "add weekly meeting every Monday")
- Chatbot MUST handle reminder creation (e.g., "remind me about groceries at 5 PM")
- Chatbot MUST support tag/category management (e.g., "tag task 3 as work")
- Intent recognition MUST handle common task management phrases
- Chatbot MUST provide clear feedback for successful and failed operations
- Ambiguous inputs MUST prompt for clarification rather than guess incorrectly
- OpenAI Agents SDK MUST be used for NLP processing

**Rationale**: The chatbot reduces friction in task management by allowing users to interact naturally, even for advanced features like recurring tasks and reminders.

### III. API-Driven Architecture

All functionality MUST be exposed through well-defined REST API endpoints. The chatbot and frontend are consumers of the same backend API.

**Rules**:
- Backend MUST expose task CRUD operations as RESTful endpoints
- Backend MUST expose search, filter, and sort capabilities via query parameters
- Backend MUST expose recurring task and reminder management endpoints
- Chatbot MUST communicate with backend via the same API as the frontend
- API contracts MUST be documented and versioned
- No direct database access from frontend or chatbot layers
- FastAPI MUST be used for backend API implementation
- SQLModel MUST be used for database models with Neon PostgreSQL

**Rationale**: A unified API ensures consistency, enables independent frontend/chatbot development, and simplifies testing.

### IV. Test-Driven Development

Critical paths MUST have automated tests. Test coverage ensures reliability as the system evolves.

**Rules**:
- API endpoints MUST have contract tests validating request/response schemas
- Authentication flows MUST have integration tests
- Chatbot intent parsing MUST have unit tests for common phrases
- Database operations MUST have tests verifying data integrity
- Recurring task auto-creation MUST have tests verifying next occurrence logic
- Tests SHOULD be written before or alongside implementation

**Rationale**: The chatbot-task integration has many failure points. Tests catch regressions early and document expected behavior.

### V. Performance & Responsiveness

The system MUST provide smooth, responsive interaction for multiple concurrent users with event-driven processing.

**Rules**:
- API response time MUST be under 500ms for standard operations (p95)
- Chatbot response time MUST be under 2 seconds including NLP processing
- Database queries MUST use appropriate indexes for user-scoped queries
- Search queries MUST use database-level text matching for efficiency
- Frontend MUST show loading states during async operations
- Event publishing MUST NOT block the main request/response cycle
- Kafka message processing latency SHOULD be under 1 second

**Rationale**: Slow responses break conversational flow and frustrate users. Performance is a feature. Event-driven processing enables non-blocking advanced features.

### VI. Secure Authentication

JWT-based authentication MUST protect all user operations. Security is mandatory, not optional.

**Rules**:
- All task API endpoints MUST require valid JWT authentication
- JWTs MUST include user ID for ownership validation
- Token expiration MUST be enforced; refresh tokens MUST be supported
- Password storage MUST use bcrypt or equivalent secure hashing
- HTTPS MUST be used in production environments
- Chatbot sessions MUST be linked to authenticated users
- Kubernetes secrets MUST be used for sensitive configuration in deployment

**Rationale**: Task data is personal. Unauthenticated access or weak auth exposes user data to attackers.

### VII. Intelligent Task Organization

Tasks MUST support rich metadata for organization, discovery, and automation.

**Rules**:
- Tasks MUST support tags/categories as flexible labels (e.g., work, home, personal)
- Tasks MUST support priority levels (low, medium, high, urgent)
- Tasks MUST be searchable by keyword across title and description
- Tasks MUST be sortable by due date, priority, creation date, or title
- Tasks MUST support filtering by any combination of status, priority, tags, and date range
- Recurring tasks MUST automatically create the next occurrence when completed
- Recurrence patterns MUST support: daily, weekly, monthly, yearly
- Due date reminders MUST be configurable per task

**Rationale**: As task lists grow, users need powerful organization tools. Tags, search, sort, and recurrence transform a simple list into an intelligent task management system.

### VIII. Event-Driven Architecture

The system MUST use event-driven patterns for decoupled, scalable processing of advanced features.

**Rules**:
- Task CRUD operations MUST publish events to Kafka topics
- Recurring task auto-creation MUST be handled by an event consumer, not inline
- Reminder/notification delivery MUST be handled by a dedicated consumer service
- Event schemas MUST include: event_type, task_id, user_id, task_data, timestamp
- Kafka topics: `task-events`, `reminders`, `task-updates`
- Producers MUST NOT wait for consumer acknowledgment (fire-and-forget for non-critical)
- Consumer failures MUST NOT affect the main API request/response

**Rationale**: Event-driven architecture decouples features like reminders and recurring tasks from the core API, improving reliability and scalability.

### IX. Distributed Application Runtime (Dapr)

Dapr MUST be used to abstract infrastructure dependencies and enable portable microservices.

**Rules**:
- Dapr Pub/Sub MUST abstract Kafka for event publishing/subscribing
- Dapr State Management MAY be used for conversation state caching
- Dapr Service Invocation MUST be used for inter-service communication in K8s
- Dapr Bindings (cron) MUST be used for scheduled reminder checks
- Dapr Secrets Management MUST be used for API keys and credentials in K8s
- Application code MUST interact with Dapr via HTTP APIs (localhost:3500)
- Swapping infrastructure components MUST require only YAML config changes, not code changes

**Rationale**: Dapr abstracts infrastructure (Kafka, DB, Secrets) behind simple HTTP APIs. This enables vendor-agnostic, portable microservices that work identically on Minikube and cloud K8s.

### X. Cloud-Native Deployment

The system MUST be deployable on both local Minikube and production cloud Kubernetes.

**Rules**:
- All services MUST be containerized with Docker
- Helm charts MUST be used for Kubernetes deployment configuration
- CI/CD pipeline MUST use GitHub Actions for automated deployment
- Monitoring and logging MUST be configured for production observability
- Local development MUST work on Minikube with identical Helm charts
- Cloud deployment MUST target DigitalOcean DOKS (or GKE/AKS)
- Environment-specific configuration MUST be handled via Helm values files

**Rationale**: Cloud-native deployment ensures the application scales reliably and can be managed using standard Kubernetes tooling across any provider.

## Technology Stack

The following technologies are mandated for this project:

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Next.js, React, TypeScript | User interface and chatbot widget |
| Backend | FastAPI | REST API server |
| ORM | SQLModel | Database models and queries |
| Database | Neon PostgreSQL | Persistent data storage |
| AI/NLP | OpenAI Agents SDK | Chatbot natural language processing |
| Auth | JWT (python-jose, passlib) | Authentication and authorization |
| Event Streaming | Kafka (Redpanda) | Event-driven architecture |
| Runtime | Dapr | Distributed application runtime (sidecar) |
| Containerization | Docker | Application packaging |
| Orchestration | Kubernetes (Minikube + DOKS) | Container orchestration |
| Package Manager | Helm Charts | K8s deployment configuration |
| CI/CD | GitHub Actions | Automated deployment pipeline |

**Constraints**:
- TypeScript MUST be used for frontend code
- Python 3.11+ MUST be used for backend code
- Environment variables MUST be used for secrets (never hardcoded)
- Dapr sidecar MUST be used for infrastructure abstraction in K8s

## Feature Levels

### Basic Level (Phases I-IV) - COMPLETE
- [x] Add Task
- [x] Delete Task
- [x] Update Task
- [x] View Task List
- [x] Mark as Complete
- [x] AI Chatbot Interface
- [x] Local Kubernetes Deployment

### Intermediate Level (Phase V)
- [ ] Priorities & Tags/Categories
- [ ] Search & Filter (keyword, status, priority, date)
- [ ] Sort Tasks (due date, priority, alphabetically)

### Advanced Level (Phase V)
- [ ] Recurring Tasks (daily, weekly, monthly, yearly)
- [ ] Due Dates & Time Reminders (browser notifications)
- [ ] Event-Driven Architecture (Kafka)
- [ ] Dapr Integration (Pub/Sub, State, Bindings, Secrets)
- [ ] Cloud Deployment (DOKS/GKE/AKS)

## Development Workflow

### Code Quality Gates

1. **Pre-commit**: Linting (ESLint, Ruff) and formatting (Prettier, Black) MUST pass
2. **PR Review**: All changes MUST be reviewed before merge
3. **CI Pipeline**: Tests MUST pass before merge to main branch
4. **Security Scan**: Dependencies MUST be scanned for known vulnerabilities

### Branch Strategy

- `main`: Production-ready code only
- `feature/*`: New feature development
- `fix/*`: Bug fixes
- `docs/*`: Documentation updates

### Commit Standards

- Commits MUST follow Conventional Commits format
- Example: `feat(tasks): add recurring task auto-creation on completion`
- Co-authored commits with AI assistance MUST include AI attribution

## Governance

This constitution is the authoritative source for project principles and standards.

### Amendment Process

1. Propose amendment with rationale
2. Document impact on existing code and templates
3. Update version according to semantic versioning:
   - MAJOR: Principle removal or incompatible redefinition
   - MINOR: New principle or material expansion
   - PATCH: Clarification or typo fix
4. Update dependent templates if affected
5. Commit with message: `docs: amend constitution to vX.Y.Z`

### Compliance

- All PRs MUST verify alignment with these principles
- Architecture Decision Records (ADRs) MUST reference relevant principles
- Complexity beyond these standards MUST be justified in writing

### Review Schedule

- Constitution review: Quarterly or upon major feature completion
- Principle relevance check: Before each major release

**Version**: 2.0.0 | **Ratified**: 2025-02-05 | **Last Amended**: 2026-02-08
