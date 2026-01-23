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