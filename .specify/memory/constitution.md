<<<<<<< HEAD
# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

### [PRINCIPLE_6_NAME]


[PRINCIPLE__DESCRIPTION]

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
=======
<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0
Modified principles: [PRINCIPLE_1_NAME] → SPEC-DRIVEN DEVELOPMENT, [PRINCIPLE_2_NAME] → NO MANUAL CODE RULE, [PRINCIPLE_3_NAME] → AGENTIC DEVELOPMENT MODEL, [PRINCIPLE_4_NAME] → TECHNOLOGY STACK LOCK, [PRINCIPLE_5_NAME] → PHASE ISOLATION RULES, [PRINCIPLE_6_NAME] → MONOREPO STRUCTURE
Added sections: API & AUTHENTICATION RULES, WORKFLOW (STRICT ORDER), FINAL RULE
Removed sections: None
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Hackathon II – The Evolution of Todo Constitution

## Core Principles

### SPEC-DRIVEN DEVELOPMENT (MANDATORY)
Every feature MUST begin with a written specification inside /specs. No code may be generated without referencing an approved spec. Specs MUST define user stories, acceptance criteria, API behavior, and security/auth rules. Missing requirements MUST be fixed in specs before implementation.

### NO MANUAL CODE RULE
Humans MUST NOT write application code. Humans MAY ONLY write or refine specs, review generated output, and request changes by updating specs. Editing generated code directly is forbidden.

### AGENTIC DEVELOPMENT MODEL
The system MUST operate using specialized agents and skills: Orchestrator Agent coordinates workflow and enforces excellence; Spec Manager Agent owns and writes all specifications; Backend Agent implements FastAPI, SQLModel, Neon DB, JWT verification; Frontend Agent implements Next.js App Router UI and Better Auth integration; Constitution Keeper enforces this Constitution and blocks violations. Agents MUST stay within their defined responsibilities.

### TECHNOLOGY STACK (LOCKED FOR PHASE II)
Frontend: Next.js (App Router), TypeScript, Tailwind CSS, Better Auth (signup / signin). Backend: Python FastAPI, SQLModel ORM. Database: Neon Serverless PostgreSQL. Authentication: Better Auth on frontend, JWT-based authentication, Shared secret via environment variables, Backend MUST independently verify JWT tokens. Spec System: Spec-Kit Plus, Claude Code.

### PHASE ISOLATION RULES
Phase I: In-memory console application only, No database, No authentication, No web UI. Phase II: Web frontend is allowed, Authentication is allowed, Neon PostgreSQL is allowed, Full-stack architecture is allowed. Phase III and later: AI chatbots, Advanced agents, Cloud-native orchestration. No future-phase technology is allowed in Phase II.

### MONOREPO STRUCTURE (MANDATORY)
/.spec-kit/config.yaml, /specs/overview.md, architecture.md, /features/, /api/, /database/, /ui/, /frontend/, /backend/, /CLAUDE.md, /frontend/CLAUDE.md, /backend/CLAUDE.md. Claude Code MUST reference specs using @specs/[path]/[file].md.

## API & AUTHENTICATION RULES
All API endpoints MUST be secured. Every request MUST include Authorization: Bearer <JWT>. Backend MUST extract JWT from headers, verify token using shared secret, decode user identity from token, NEVER trust user_id from URL alone. Each user MUST only access their own tasks. Violations are CRITICAL.

## WORKFLOW (STRICT ORDER)
1. Write or update spec
2. Reference the spec
3. Ask Claude Code to implement
4. Review output
5. Fix by updating specs, NOT code

Skipping any step is forbidden.

## FINAL RULE
If there is EVER a conflict between human instruction, generated code, or Project Constitution, the PROJECT CONSTITUTION ALWAYS WINS.

## Governance
This Constitution is the SINGLE SOURCE OF TRUTH. Any deviation is a CRITICAL VIOLATION. All implementation must verify compliance with these principles. This document supersedes all other practices and guidelines.

**Version**: 2.0.0 | **Ratified**: 2026-01-18 | **Last Amended**: 2026-01-18
>>>>>>> 4c9a8fb (Fix redirect after auth - dashboard now redirects to main todo app)
