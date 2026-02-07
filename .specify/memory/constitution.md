<!--
  ============================================================================
  SYNC IMPACT REPORT
  ============================================================================
  Version Change: (new) → 1.0.0

  Added Principles:
    - I. User Data Isolation (NEW)
    - II. AI-First Interaction (NEW)
    - III. API-Driven Architecture (NEW)
    - IV. Test-Driven Development (NEW)
    - V. Performance & Responsiveness (NEW)
    - VI. Secure Authentication (NEW)

  Added Sections:
    - Technology Stack (NEW)
    - Development Workflow (NEW)
    - Governance (NEW)

  Removed Sections: None (initial constitution)

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

**Rationale**: User privacy and data security are foundational to trust. A multi-tenant task system without strict isolation is a security vulnerability.

### II. AI-First Interaction

The chatbot is the primary interface for task management. Natural language processing MUST provide intuitive task operations.

**Rules**:
- Chatbot MUST support Create, View, Update, and Delete operations via natural language
- Intent recognition MUST handle common task management phrases (e.g., "add", "show", "complete", "remove")
- Chatbot MUST provide clear feedback for successful and failed operations
- Ambiguous inputs MUST prompt for clarification rather than guess incorrectly
- OpenAI Agents SDK MUST be used for NLP processing

**Rationale**: The chatbot reduces friction in task management by allowing users to interact naturally without navigating complex UIs.

### III. API-Driven Architecture

All functionality MUST be exposed through well-defined REST API endpoints. The chatbot and frontend are consumers of the same backend API.

**Rules**:
- Backend MUST expose task CRUD operations as RESTful endpoints
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
- Tests SHOULD be written before or alongside implementation

**Rationale**: The chatbot-task integration has many failure points. Tests catch regressions early and document expected behavior.

### V. Performance & Responsiveness

The system MUST provide smooth, responsive interaction for multiple concurrent users.

**Rules**:
- API response time MUST be under 500ms for standard operations (p95)
- Chatbot response time MUST be under 2 seconds including NLP processing
- Database queries MUST use appropriate indexes for user-scoped queries
- Frontend MUST show loading states during async operations
- WebSocket or polling MAY be used for real-time updates

**Rationale**: Slow responses break conversational flow and frustrate users. Performance is a feature.

### VI. Secure Authentication

JWT-based authentication MUST protect all user operations. Security is mandatory, not optional.

**Rules**:
- All task API endpoints MUST require valid JWT authentication
- JWTs MUST include user ID for ownership validation
- Token expiration MUST be enforced; refresh tokens MUST be supported
- Password storage MUST use bcrypt or equivalent secure hashing
- HTTPS MUST be used in production environments
- Chatbot sessions MUST be linked to authenticated users

**Rationale**: Task data is personal. Unauthenticated access or weak auth exposes user data to attackers.

## Technology Stack

The following technologies are mandated for this project:

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Next.js, React | User interface and chatbot widget |
| Backend | FastAPI | REST API server |
| ORM | SQLModel | Database models and queries |
| Database | Neon PostgreSQL | Persistent data storage |
| AI/NLP | OpenAI Agents SDK | Chatbot natural language processing |
| Auth | JWT (python-jose, passlib) | Authentication and authorization |

**Constraints**:
- TypeScript MUST be used for frontend code
- Python 3.11+ MUST be used for backend code
- Environment variables MUST be used for secrets (never hardcoded)

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
- Example: `feat(chatbot): add task creation via natural language`
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

**Version**: 1.0.0 | **Ratified**: 2025-02-05 | **Last Amended**: 2025-02-05
