# Implementation Plan: AI-Powered Chatbot Frontend

**Branch**: `002-chatbot-frontend` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-chatbot-frontend/spec.md`

## Summary

Build a Next.js frontend application that provides an AI-powered conversational interface for managing todo tasks. Users authenticate with JWT tokens, interact with a chatbot to create, view, filter, update, and complete tasks using natural language commands. The interface is mobile-first and responsive across all device sizes, connecting to the existing FastAPI backend that handles task CRUD operations and chatbot NLP processing.

**Primary Requirement**: Deliver a conversational task management interface that reduces friction compared to traditional form-based UIs while maintaining secure user authentication and data isolation.

**Technical Approach**: Use Next.js 14+ with App Router for server-side rendering and routing, React 18+ for UI components, Tailwind CSS for responsive styling, and Axios for authenticated API calls to the backend. Implement JWT token management with automatic refresh, real-time chat interface with typing indicators, and mobile-optimized layouts using CSS Grid and Flexbox.

## Technical Context

**Language/Version**: TypeScript 5.x with Next.js 14+ (App Router), React 18+
**Primary Dependencies**: Next.js, React, Tailwind CSS, Axios (HTTP client), React Hook Form (form validation), date-fns (date formatting)
**Storage**: Browser localStorage for JWT tokens (access and refresh tokens)
**Testing**: Jest for unit tests, React Testing Library for component tests, Playwright or Cypress for E2E tests
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - last 2 versions), Mobile web (iOS Safari, Android Chrome)
**Project Type**: Web (frontend only - connects to existing backend)
**Performance Goals**:
- Initial page load < 3 seconds on 3G networks
- Time to Interactive (TTI) < 5 seconds
- Chat message round-trip < 2 seconds (including API call)
- 60fps scroll performance on mobile devices
**Constraints**:
- Must work on mobile viewports as small as 375px width
- Touch targets must be minimum 44x44px for mobile accessibility
- Must handle JWT token expiry gracefully with automatic refresh
- No backend modifications allowed (consume existing API as-is)
**Scale/Scope**:
- Single-user sessions (no real-time collaboration)
- Support up to 1000 tasks per user with pagination
- Chat history stored in-memory (session-scoped, not persisted)
- 5-10 frontend pages/routes (login, register, chat, settings)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: User Data Isolation ✅ PASS

**How frontend ensures compliance**:
- JWT access token (containing user ID) is automatically attached to all API requests via Axios interceptor
- Frontend never stores or caches other users' data
- Chat interface only displays tasks returned by authenticated API calls scoped to current user
- Token validation happens on backend; frontend trusts backend to enforce user isolation

**Verification**: API calls include `Authorization: Bearer <token>` header; backend validates user ownership

---

### Principle II: AI-First Interaction ✅ PASS

**How frontend supports AI interaction**:
- Chatbot interface is the primary view (not buried in settings)
- Message input accepts natural language commands (e.g., "create task to buy groceries tomorrow")
- Chatbot responses are formatted with rich UI (icons, colors, task cards)
- Help command (`help` or `?`) displays supported natural language patterns
- Clarification flows handled via conversational prompts from backend

**Verification**: User can complete task creation/viewing without clicking any buttons except "Send"

---

### Principle III: API-Driven Architecture ✅ PASS

**How frontend consumes API**:
- All task operations go through backend REST API (`POST /api/chat/message`, `GET /api/tasks`, etc.)
- No direct database access from frontend (impossible in browser environment)
- API client module (`services/api.ts`) centralizes all backend communication
- OpenAPI/TypeScript types generated from backend contracts ensure type safety

**Verification**: Network tab shows all operations as HTTP requests to backend; no local DB access

---

### Principle IV: Test-Driven Development ✅ PASS

**Frontend testing strategy**:
- **Unit tests**: Individual React components (Button, MessageBubble, TaskCard) with Jest + React Testing Library
- **Integration tests**: Authentication flows (login → token storage → authenticated request)
- **Component tests**: Chat interface (message send → loading state → response display)
- **E2E tests**: Full user journeys (register → create task → view task → logout) with Playwright
- **Contract tests**: Verify API request/response schemas match backend expectations

**Verification**: Test coverage >70% for critical paths (auth, chat, task display)

---

### Principle V: Performance & Responsiveness ✅ PASS

**Frontend performance measures**:
- **Code splitting**: Next.js dynamic imports for non-critical components
- **Image optimization**: Next.js Image component with lazy loading
- **Loading states**: Skeleton screens and spinners for all async operations
- **Debouncing**: Input debounce (300ms) prevents excessive API calls while typing
- **Caching**: React Query or SWR for client-side caching of task lists (reduces redundant API calls)
- **Optimistic updates**: UI updates immediately, rolls back on error

**Verification**: Lighthouse score >90 for Performance; no janky scrolling on mobile

---

### Principle VI: Secure Authentication ✅ PASS

**Frontend authentication implementation**:
- JWT tokens stored in localStorage (access token) and secure httpOnly cookies (ideal, but localStorage acceptable per spec assumptions)
- Axios interceptor auto-attaches `Authorization` header to all requests
- Token refresh logic: on 401 error, attempt refresh with refresh token before forcing re-login
- Protected routes: useAuth hook redirects to login if no valid token
- Logout clears all tokens from storage and redirects to login page
- No sensitive data (passwords) stored in frontend state or storage

**Verification**:
- Network requests include Authorization header
- Expired token triggers automatic refresh or login redirect
- Logout clears localStorage and navigates to /login

---

**Constitution Check Summary**: ✅ ALL PRINCIPLES PASS

No violations requiring justification. The frontend architecture aligns with all six principles.

## Project Structure

### Documentation (this feature)

```text
specs/002-chatbot-frontend/
├── plan.md              # This file (/sp.plan output)
├── research.md          # Phase 0 output (frontend tech decisions)
├── data-model.md        # Phase 1 output (frontend state model)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts & TypeScript types)
│   ├── auth.yaml        # Authentication endpoints
│   ├── chat.yaml        # Chatbot endpoints
│   └── tasks.yaml       # Task CRUD endpoints
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created yet)
```

### Source Code (repository root)

```text
frontend/                         # Next.js application root
├── app/                          # Next.js 14 App Router
│   ├── (auth)/                   # Auth route group (no nav)
│   │   ├── login/
│   │   │   └── page.tsx          # Login page
│   │   └── register/
│   │       └── page.tsx          # Registration page
│   ├── (chat)/                   # Chat route group (with nav)
│   │   ├── layout.tsx            # Chat layout with navbar
│   │   └── page.tsx              # Main chatbot interface
│   ├── layout.tsx                # Root layout (providers, fonts)
│   ├── globals.css               # Tailwind base styles
│   └── api/                      # API routes (if needed for proxying)
│
├── components/                   # Reusable React components
│   ├── auth/
│   │   ├── LoginForm.tsx         # Login form component
│   │   ├── RegisterForm.tsx      # Registration form component
│   │   └── ProtectedRoute.tsx    # Auth guard HOC
│   ├── chat/
│   │   ├── ChatInterface.tsx     # Main chat container
│   │   ├── MessageList.tsx       # Chat message history
│   │   ├── MessageBubble.tsx     # Single message bubble
│   │   ├── MessageInput.tsx      # Text input with send button
│   │   ├── TypingIndicator.tsx   # Loading/typing animation
│   │   └── TaskCard.tsx          # Task display in chat
│   ├── layout/
│   │   ├── Header.tsx            # App header/navbar
│   │   └── Footer.tsx            # App footer
│   └── ui/                       # Generic UI primitives
│       ├── Button.tsx
│       ├── Input.tsx
│       ├── Spinner.tsx
│       └── ErrorMessage.tsx
│
├── services/                     # API and business logic
│   ├── api.ts                    # Axios instance with interceptors
│   ├── auth.service.ts           # Auth API calls (login, register, refresh)
│   ├── chat.service.ts           # Chatbot API calls
│   └── task.service.ts           # Task CRUD API calls
│
├── hooks/                        # Custom React hooks
│   ├── useAuth.ts                # Authentication state management
│   ├── useChat.ts                # Chat state and message handling
│   └── useTasks.ts               # Task list state (optional caching)
│
├── lib/                          # Utility functions
│   ├── token.ts                  # JWT token storage/retrieval
│   ├── validators.ts             # Input validation helpers
│   └── formatters.ts             # Date/time formatting
│
├── types/                        # TypeScript type definitions
│   ├── api.types.ts              # API request/response types
│   ├── auth.types.ts             # Auth-related types
│   ├── chat.types.ts             # Chat message types
│   └── task.types.ts             # Task entity types
│
├── contexts/                     # React Context providers
│   └── AuthContext.tsx           # Global auth state provider
│
├── tests/                        # Test files
│   ├── unit/
│   │   └── components/           # Component unit tests
│   ├── integration/
│   │   └── auth.test.ts          # Auth flow integration tests
│   └── e2e/
│       └── chat.spec.ts          # E2E chat tests with Playwright
│
├── public/                       # Static assets
│   ├── images/
│   └── icons/
│
├── tailwind.config.ts            # Tailwind configuration
├── tsconfig.json                 # TypeScript configuration
├── next.config.js                # Next.js configuration
├── package.json                  # Dependencies
└── .env.local.example            # Environment variables template
```

**Structure Decision**: Web application structure with frontend-only codebase. The frontend is a standalone Next.js application that consumes the existing FastAPI backend API. We use the Next.js 14 App Router for file-based routing and server components, separating concerns into components (UI), services (API calls), hooks (state logic), and contexts (global state). This structure supports code splitting, TypeScript type safety, and independent component testing.

## Complexity Tracking

> **No violations - this section intentionally left empty**

All complexity remains within constitutional bounds. No additional justification required.

## Architecture Decisions

### AD-001: Next.js 14 with App Router vs Pages Router

**Decision**: Use Next.js 14 App Router (not Pages Router)

**Rationale**:
- Server components reduce client-side JavaScript bundle size
- Improved routing with layouts and loading states
- Better data fetching patterns with React Server Components
- Forward-looking (Pages Router is legacy)

**Alternatives Considered**:
- **Pages Router**: More mature, wider ecosystem support, but deprecated in favor of App Router
- **Create React App (CRA)**: Simpler setup, but lacks SSR, image optimization, and performance features
- **Vite + React**: Faster dev server, but requires manual configuration for routing, SSR, image optimization

**Trade-offs**:
- Steeper learning curve for App Router (newer paradigm)
- Some libraries may not fully support React Server Components yet
- Mitigation: Use client components (`'use client'`) for interactive chat interface

---

### AD-002: Tailwind CSS vs CSS Modules vs Styled Components

**Decision**: Use Tailwind CSS for styling

**Rationale**:
- Mobile-first utility classes simplify responsive design (critical for FR-019, FR-020)
- Smaller CSS bundle (unused styles purged at build time)
- Consistent design system via Tailwind config (colors, spacing, breakpoints)
- Excellent DX with autocomplete in VS Code

**Alternatives Considered**:
- **CSS Modules**: Type-safe, but requires more boilerplate; less DX for responsive variants
- **Styled Components**: CSS-in-JS with dynamic styling, but adds runtime overhead and doesn't work well with Server Components
- **Plain CSS**: Maximum flexibility, but poor DX and no built-in responsive utilities

**Trade-offs**:
- HTML becomes verbose with many utility classes
- Mitigation: Extract component classes into reusable React components

---

### AD-003: JWT Storage in localStorage vs httpOnly Cookies

**Decision**: Store JWT tokens in localStorage (per spec assumptions)

**Rationale**:
- Spec assumption #4 explicitly states localStorage is acceptable
- Simpler implementation (no cookie configuration needed)
- Tokens accessible to Axios interceptors for Authorization headers
- Refresh token flow works client-side without backend cookie handling

**Alternatives Considered**:
- **httpOnly Cookies**: More secure against XSS attacks, but requires backend to set cookies (backend modification not allowed per spec)
- **sessionStorage**: Cleared on tab close (not persistent), doesn't meet "stay logged in" UX expectation
- **In-memory state only**: Lost on page refresh, poor UX

**Trade-offs**:
- Vulnerable to XSS attacks if malicious scripts access localStorage
- Mitigation: Implement Content Security Policy (CSP) headers, input sanitization, and avoid eval()

---

### AD-004: Chat History Persistence

**Decision**: Chat history is in-memory (session-scoped, not persisted to backend or localStorage)

**Rationale**:
- Spec does not require chat history persistence
- Reduces backend API surface (no chat history endpoints needed)
- Simpler frontend state management (just React state)
- Privacy-friendly (no chat logs stored)

**Alternatives Considered**:
- **localStorage**: Persist chat across page refreshes, but increases localStorage size and complexity
- **Backend storage**: Full chat history with timestamps, but requires new API endpoints and DB schema (out of scope)

**Trade-offs**:
- Page refresh clears chat history, requiring users to scroll up to see old conversations
- Mitigation: Document this behavior as expected in UX; consider localStorage in future iterations if user feedback indicates need

---

### AD-005: State Management: Context API vs Redux vs Zustand

**Decision**: Use React Context API for auth state + local component state for chat

**Rationale**:
- Auth state is global (needed across app) → Context API sufficient
- Chat state is component-scoped (only used in chat interface) → local useState is simplest
- No complex state interactions requiring Redux/Zustand

**Alternatives Considered**:
- **Redux Toolkit**: Overkill for this scope; adds boilerplate for time-travel debugging we don't need
- **Zustand**: Lightweight, but unnecessary when Context API + useState handles our needs

**Trade-offs**:
- Context API can cause unnecessary re-renders if not optimized
- Mitigation: Split AuthContext into separate provider and consumer; use React.memo for expensive components

---

### AD-006: API Client: Axios vs Fetch API

**Decision**: Use Axios for HTTP requests

**Rationale**:
- Interceptors for auto-attaching Authorization headers
- Interceptors for automatic token refresh on 401 errors
- Better error handling with structured error objects
- Request/response transformation built-in

**Alternatives Considered**:
- **Fetch API**: Native browser API, no dependencies, but requires manual interceptor logic and more boilerplate

**Trade-offs**:
- Adds 13KB to bundle size (minified + gzipped)
- Mitigation: Bundle size is acceptable for DX gains

---

### AD-007: Date Handling: date-fns vs Moment.js vs Luxon

**Decision**: Use date-fns for date formatting and parsing

**Rationale**:
- Tree-shakable (only import functions you use)
- Immutable (no mutation bugs)
- TypeScript support
- Smaller bundle than Moment.js

**Alternatives Considered**:
- **Moment.js**: Large bundle (deprecated), mutable APIs
- **Luxon**: Good alternative, but slightly larger than date-fns for our use case
- **Native Date**: No dependencies, but inconsistent browser support for formatting and timezones

**Trade-offs**:
- Need to import individual functions (e.g., `format`, `parseISO`)
- Mitigation: Create utility wrapper functions in `lib/formatters.ts`

## Implementation Phases

### Phase 0: Research & Decision Validation ✅ COMPLETE
- All architecture decisions documented above
- No NEEDS CLARIFICATION items remain
- Output: This plan.md file

### Phase 1: Design & Contracts (Next)
- Generate data-model.md (frontend state model)
- Generate API contracts (auth.yaml, chat.yaml, tasks.yaml)
- Generate quickstart.md (setup instructions)
- Update agent context with frontend tech stack

### Phase 2: Task Breakdown (/sp.tasks command)
- Generate tasks.md with implementation tasks
- Prioritize tasks by user story (P1, P2, P3)
- Define acceptance criteria per task

### Phase 3: Implementation (Execute tasks)
- Execute tasks from tasks.md
- Write tests alongside implementation
- Deploy to preview environment

### Phase 4: Testing & Validation
- Run E2E tests
- Lighthouse performance audit
- Mobile device testing (real devices)
- Security review (CSP, XSS protection)

## Dependencies

### Backend API (CRITICAL - Must exist before frontend work begins)

The frontend depends on the following backend endpoints being fully implemented and available:

**Authentication Endpoints**:
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Token refresh
- `POST /auth/logout` - Logout (optional, client-side token clearing sufficient)

**Chatbot Endpoints**:
- `POST /api/chat/message` - Send message to chatbot

**Task Endpoints** (if direct access needed, though chatbot should handle most):
- `GET /api/tasks` - List user's tasks with filters (status, priority, due_before, pagination)
- `POST /api/tasks` - Create task directly (fallback if chatbot fails)
- `GET /api/tasks/{id}` - Get single task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/complete` - Mark task complete
- `DELETE /api/tasks/{id}` - Delete task (soft delete)

**Backend Status**: ✅ CONFIRMED - Backend implementation completed in previous phase (001-chatbot-task-api)

### External Dependencies

**NPM Packages** (installed via `npm install`):
- `next` ^14.0.0 - Next.js framework
- `react` ^18.0.0 - React library
- `react-dom` ^18.0.0 - React DOM renderer
- `typescript` ^5.0.0 - TypeScript
- `tailwindcss` ^3.4.0 - Utility-first CSS framework
- `axios` ^1.6.0 - HTTP client
- `react-hook-form` ^7.49.0 - Form validation
- `date-fns` ^3.0.0 - Date formatting
- `@headlessui/react` ^1.7.0 - Unstyled accessible components (modals, dropdowns)
- `lucide-react` - Icon library

**Dev Dependencies**:
- `@types/react`, `@types/node` - TypeScript types
- `jest`, `@testing-library/react` - Testing
- `@playwright/test` - E2E testing
- `eslint`, `prettier` - Linting and formatting

### Browser Requirements

**Minimum Supported Browsers**:
- Chrome 90+ (released 2021)
- Firefox 88+ (released 2021)
- Safari 14+ (iOS 14+, released 2020)
- Edge 90+ (released 2021)

**Rationale**: Last 2 years of browser releases per spec assumption #3

## Risk Mitigation

### Technical Risks

**Risk 1: JWT Token Security (localStorage XSS vulnerability)**
- **Likelihood**: Medium (if XSS vulnerability exists)
- **Impact**: High (attacker can steal tokens and impersonate users)
- **Mitigation**:
  - Implement Content Security Policy (CSP) headers to block inline scripts
  - Sanitize all user inputs (especially chat messages)
  - Use React's built-in XSS protection (JSX escapes by default)
  - Avoid `dangerouslySetInnerHTML` unless absolutely necessary
  - Short token expiry (1 hour) limits damage window
- **Contingency**: Future iteration could migrate to httpOnly cookies if backend supports it

**Risk 2: Token Refresh Race Conditions**
- **Likelihood**: Medium (multiple API calls during token expiry)
- **Impact**: Medium (duplicate refresh requests, potential 401 errors)
- **Mitigation**:
  - Implement token refresh queue in Axios interceptor
  - Queue subsequent requests while refresh is in progress
  - Retry queued requests with new token after refresh completes
- **Contingency**: Add retry logic with exponential backoff

**Risk 3: Mobile Keyboard Obscuring Input Field**
- **Likelihood**: High (iOS Safari specifically)
- **Impact**: Medium (poor UX, users can't see what they're typing)
- **Mitigation**:
  - Use `window.visualViewport` API to detect keyboard height
  - Adjust chat container height dynamically
  - Scroll input field into view when keyboard opens
  - Test on real iOS and Android devices
- **Contingency**: Provide "full screen" chat mode as fallback

**Risk 4: Chatbot NLP Misinterpretation**
- **Likelihood**: Medium (ambiguous natural language)
- **Impact**: Low to Medium (wrong task created, user frustration)
- **Mitigation**:
  - Display confirmation UI before submitting ambiguous commands
  - Show extracted parameters (title, priority, due date) for user verification
  - Provide "Undo" action for recent task creations
  - Help command shows clear examples of supported syntax
- **Contingency**: Fallback to form-based task creation in future iteration

### User Experience Risks

**Risk 5: Slow Network Performance (3G/4G)**
- **Likelihood**: Medium (mobile users on slow networks)
- **Impact**: High (poor UX, perceived lag)
- **Mitigation**:
  - Implement optimistic UI updates (instant feedback before API confirms)
  - Show loading skeletons instead of blank screens
  - Code splitting to reduce initial bundle size
  - Compress images and assets
  - Use CDN for static assets (Vercel Edge Network)
- **Contingency**: Offline mode with service workers in future iteration

**Risk 6: Learning Curve for Chatbot Interface**
- **Likelihood**: High (users unfamiliar with conversational UIs)
- **Impact**: Medium (slow adoption, support requests)
- **Mitigation**:
  - Prominent "Help" button showing command examples
  - Placeholder text in input with example command ("Try: create task to buy groceries")
  - Quick action buttons for common tasks (optional, future iteration)
  - Onboarding tutorial on first login
- **Contingency**: Add traditional list view alongside chatbot as alternative interface

### Business Risks

**Risk 7: Backend Downtime**
- **Likelihood**: Low to Medium
- **Impact**: High (frontend unusable)
- **Mitigation**:
  - Clear error messaging when backend is unreachable
  - Retry failed requests with exponential backoff
  - Health check endpoint (`GET /health`) polled periodically
  - Display maintenance mode banner when backend is down
- **Contingency**: Static error page with estimated recovery time

**Risk 8: Third-Party Dependency Vulnerabilities**
- **Likelihood**: Medium (NPM packages regularly have CVEs)
- **Impact**: High (security vulnerabilities)
- **Mitigation**:
  - Run `npm audit` in CI/CD pipeline
  - Dependabot alerts for known vulnerabilities
  - Pin major versions, auto-update patch versions
  - Regular dependency updates (quarterly)
- **Contingency**: Freeze dependencies until patches available; consider alternative packages

## Next Steps

1. ✅ **Phase 0 Complete**: Architecture decisions documented in this plan
2. **Phase 1 (Next)**: Generate data-model.md, API contracts, quickstart.md
3. **Phase 2**: Run `/sp.tasks` to generate implementation task list
4. **Phase 3**: Execute tasks, implement frontend components
5. **Phase 4**: Test, validate, deploy

**Ready for**: Phase 1 design artifacts generation
