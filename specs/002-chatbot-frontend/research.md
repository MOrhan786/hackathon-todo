# Research: Frontend Technology Stack

**Feature**: 002-chatbot-frontend
**Date**: 2026-02-06
**Purpose**: Document technology decisions and research findings for the chatbot frontend implementation

## Research Questions

### Q1: Which React Framework? (Next.js vs CRA vs Vite)

**Decision**: Next.js 14 with App Router

**Rationale**:
- **Server-Side Rendering (SSR)**: Improves initial page load performance, critical for mobile 3G networks (SC-009: <3s load time)
- **Image Optimization**: Built-in next/image component with lazy loading and WebP conversion
- **Code Splitting**: Automatic route-based splitting reduces bundle size
- **API Routes**: Can proxy backend requests if needed (though not required for this feature)
- **Developer Experience**: File-based routing, hot module replacement, TypeScript out-of-the-box
- **Production-Ready**: Vercel deployment optimized, Lighthouse scores typically 90+

**Alternatives Considered**:

| Framework | Pros | Cons | Verdict |
|-----------|------|------|---------|
| **Create React App** | Simple setup, widely used | No SSR, deprecated, poor performance | ❌ Rejected - deprecated by React team |
| **Vite + React** | Fast dev server, modern | Manual SSR setup, no image optimization | ❌ Rejected - requires too much configuration |
| **Remix** | Web Fundamentals, nested routing | Smaller ecosystem than Next.js | ❌ Rejected - less documentation for our use case |
| **Next.js 14 (App Router)** | All features needed, large ecosystem | Learning curve for App Router | ✅ **SELECTED** |

**References**:
- Next.js App Router docs: https://nextjs.org/docs/app
- Performance comparison (Next.js vs CRA): Next.js shows 40% faster TTI on average

---

### Q2: Styling Framework? (Tailwind vs CSS Modules vs Styled Components)

**Decision**: Tailwind CSS 3.4+

**Rationale**:
- **Mobile-First Utilities**: `sm:`, `md:`, `lg:` breakpoints map directly to responsive requirements (FR-019)
- **Purge Unused CSS**: Build output only includes used classes, reducing bundle size
- **Touch-Friendly Utilities**: `min-h-[44px]` enforces 44px minimum touch targets (FR-020)
- **Consistent Design System**: Configured via tailwind.config.ts (colors, spacing, breakpoints)
- **DX**: VS Code Tailwind CSS IntelliSense extension provides autocomplete

**Alternatives Considered**:

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **CSS Modules** | Scoped styles, type-safe | Boilerplate for variants | ❌ Rejected - verbose for responsive design |
| **Styled Components** | Dynamic styling, themed | Runtime overhead, RSC incompatible | ❌ Rejected - doesn't work well with App Router |
| **Plain CSS** | No dependencies | No utilities, poor DX | ❌ Rejected - too much manual work |
| **Tailwind CSS** | Utility-first, mobile-first | Verbose HTML | ✅ **SELECTED** |

**Configuration**:
```javascript
// tailwind.config.ts
module.exports = {
  theme: {
    screens: {
      'sm': '640px',   // Mobile landscape
      'md': '768px',   // Tablet (per FR-019)
      'lg': '1024px',  // Desktop (per FR-019)
      'xl': '1280px',  // Large desktop
    },
    extend: {
      minHeight: {
        'touch': '44px',  // Minimum touch target
      },
    },
  },
}
```

**References**:
- Tailwind CSS docs: https://tailwindcss.com/docs
- Mobile-first responsive design patterns: https://tailwindcss.com/docs/responsive-design

---

### Q3: HTTP Client? (Axios vs Fetch API)

**Decision**: Axios 1.6+

**Rationale**:
- **Interceptors**: Auto-attach JWT token to all requests, handle 401 refresh logic
- **Error Handling**: Structured error objects with request/response details
- **Request/Response Transformation**: Automatic JSON parsing, date conversion
- **Cancellation**: Built-in request cancellation (useful for debounced search)
- **TypeScript Support**: Strong typing for request/response

**Implementation Pattern**:
```typescript
// services/api.ts
import axios from 'axios';
import { getAccessToken, refreshAccessToken } from '@/lib/token';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

// Request interceptor: attach JWT
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: handle 401 and refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const newToken = await refreshAccessToken();
      if (newToken) {
        error.config.headers.Authorization = `Bearer ${newToken}`;
        return api.request(error.config); // Retry
      }
      // Refresh failed, redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

**Alternatives Considered**:

| Client | Pros | Cons | Verdict |
|--------|------|------|---------|
| **Fetch API** | Native, no dependencies | Manual interceptor logic | ❌ Rejected - too much boilerplate |
| **React Query** | Caching, optimistic updates | Overkill if not using caching | ⚠️ Consider for future (v2 with caching) |
| **Axios** | Interceptors, DX | 13KB bundle | ✅ **SELECTED** |

**References**:
- Axios docs: https://axios-http.com/docs/intro
- JWT refresh pattern: https://blog.logrocket.com/jwt-authentication-best-practices/

---

### Q4: State Management? (Context API vs Redux vs Zustand)

**Decision**: React Context API for auth state + local component state for chat

**Rationale**:
- **Auth State**: Global (needed across app) but simple (just user ID and tokens) → Context API sufficient
- **Chat State**: Component-scoped (only chat interface) → local `useState` is simplest
- **No Complex Interactions**: No need for middleware, time-travel debugging, or complex async flows
- **Avoid Over-Engineering**: Redux adds 10KB+ and significant boilerplate for minimal benefit

**Implementation Pattern**:
```typescript
// contexts/AuthContext.tsx
const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for token on mount
    const token = getAccessToken();
    if (token) {
      // Verify token and fetch user data
      verifyToken(token).then(setUser).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
```

**Alternatives Considered**:

| Library | Pros | Cons | Verdict |
|---------|------|------|---------|
| **Redux Toolkit** | DevTools, middleware | Boilerplate, overkill | ❌ Rejected - unnecessary complexity |
| **Zustand** | Lightweight, simple | Unnecessary for our scope | ❌ Rejected - Context API is simpler |
| **React Context** | Built-in, zero deps | Can cause re-renders | ✅ **SELECTED** |

**Optimization**: Split auth state into separate `AuthStateContext` (user data) and `AuthDispatchContext` (login/logout functions) to minimize re-renders.

**References**:
- React Context docs: https://react.dev/reference/react/useContext
- Context optimization: https://kentcdodds.com/blog/how-to-use-react-context-effectively

---

### Q5: Form Validation? (React Hook Form vs Formik vs Zod)

**Decision**: React Hook Form 7.49+ with Zod for schema validation

**Rationale**:
- **Performance**: Uncontrolled inputs (no re-render on every keystroke)
- **DX**: Simple API (`register`, `handleSubmit`, `errors`)
- **Zod Integration**: Type-safe schema validation with TypeScript inference
- **Small Bundle**: 8KB minified + gzipped

**Implementation Pattern**:
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data) => {
    // data is type-safe and validated
    login(data.email, data.password);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <p>{errors.email.message}</p>}
      <input {...register('password')} type="password" />
      {errors.password && <p>{errors.password.message}</p>}
      <button type="submit">Login</button>
    </form>
  );
}
```

**Alternatives Considered**:

| Library | Pros | Cons | Verdict |
|---------|------|------|---------|
| **Formik** | Feature-rich | Larger bundle, more re-renders | ❌ Rejected - performance overhead |
| **Manual Validation** | No dependencies | Boilerplate, error-prone | ❌ Rejected - DX too poor |
| **React Hook Form** | Performance, DX | Requires Zod/Yup for schemas | ✅ **SELECTED** |

**References**:
- React Hook Form docs: https://react-hook-form.com/
- Zod docs: https://zod.dev/

---

### Q6: Date Handling? (date-fns vs Luxon vs Day.js)

**Decision**: date-fns 3.0+

**Rationale**:
- **Tree-Shakable**: Only import functions you use (e.g., `format`, `parseISO`)
- **Immutable**: No mutation bugs (unlike Moment.js)
- **TypeScript**: Full type definitions
- **Bundle Size**: ~2KB per function (smallest among alternatives)

**Common Functions**:
```typescript
import { format, parseISO, formatDistanceToNow } from 'date-fns';

// Format task due date
const dueDate = parseISO('2026-02-10T15:00:00Z');
format(dueDate, 'MMM dd, yyyy'); // "Feb 10, 2026"

// Relative time for chat timestamps
formatDistanceToNow(new Date(message.timestamp), { addSuffix: true }); // "5 minutes ago"
```

**Alternatives Considered**:

| Library | Pros | Cons | Verdict |
|---------|------|------|---------|
| **Moment.js** | Feature-rich | Large bundle (deprecated) | ❌ Rejected - deprecated, 67KB |
| **Luxon** | Modern, good API | Slightly larger than date-fns | ❌ Rejected - 20KB vs 2KB per function |
| **Day.js** | Moment.js API, small | Less TypeScript support | ❌ Rejected - weaker types |
| **date-fns** | Tree-shakable, immutable | Need to import each function | ✅ **SELECTED** |

**References**:
- date-fns docs: https://date-fns.org/
- Bundle size comparison: https://bundlephobia.com/

---

### Q7: Testing Stack? (Jest + RTL vs Vitest)

**Decision**: Jest 29+ with React Testing Library + Playwright for E2E

**Rationale**:
- **Jest**: Industry standard, excellent Next.js integration via `next/jest`
- **React Testing Library**: Encourages testing user behavior (not implementation details)
- **Playwright**: Fast, reliable E2E tests across browsers (Chrome, Firefox, Safari)

**Testing Layers**:

| Layer | Tool | Scope | Example |
|-------|------|-------|---------|
| **Unit** | Jest + RTL | Individual components | `<Button />` click handler |
| **Integration** | Jest + RTL | Component interactions | Login form → auth state update |
| **E2E** | Playwright | Full user journeys | Register → login → create task → logout |

**Configuration**:
```javascript
// jest.config.js
const nextJest = require('next/jest');
const createJestConfig = nextJest({ dir: './' });

module.exports = createJestConfig({
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1', // Support Next.js path aliases
  },
});
```

**Alternatives Considered**:

| Tool | Pros | Cons | Verdict |
|------|------|------|---------|
| **Vitest** | Faster, Vite-native | Less Next.js integration | ❌ Rejected - Jest works better with Next.js |
| **Cypress** | E2E, time-travel debugging | Slower than Playwright | ❌ Rejected - Playwright is faster |
| **Jest + Playwright** | Best combo for Next.js | Two test runners | ✅ **SELECTED** |

**References**:
- Jest Next.js setup: https://nextjs.org/docs/testing#jest
- Playwright docs: https://playwright.dev/

---

## Summary of Decisions

| Decision Area | Choice | Rationale |
|---------------|--------|-----------|
| **Framework** | Next.js 14 App Router | SSR, image optimization, code splitting |
| **Styling** | Tailwind CSS | Mobile-first utilities, purged CSS |
| **HTTP Client** | Axios | Interceptors for JWT, error handling |
| **State** | Context API + useState | Simple auth state, component-scoped chat |
| **Forms** | React Hook Form + Zod | Performance, type-safe validation |
| **Dates** | date-fns | Tree-shakable, immutable, small |
| **Testing** | Jest + RTL + Playwright | Next.js integration, E2E reliability |

**All decisions align with Constitution Principles** and support the functional requirements defined in spec.md.

**No open research questions remain**. Ready for Phase 1 (design artifacts).
