# Fixes Applied for Chat Timeout and Hydration Errors

## Date: 2026-02-07

## Issues Resolved

### 1. Axios Timeout Error (CRITICAL)
**Problem**: Frontend API client timing out after 10 seconds when calling the chatbot endpoint.

**Root Cause**:
- The chatbot service makes **two OpenAI API calls** per message:
  1. First call to detect function/tool calls
  2. Second call to get final response after tool execution
- Each OpenAI call can take 5-10 seconds
- Database operations add additional time
- Total time often exceeds the 10-second timeout

**Fix Applied**:
```typescript
// frontend/src/services/api.ts:9
timeout: 60000, // Increased from 10000 (10s) to 60000 (60s)
```

**File Modified**: `frontend/src/services/api.ts`

---

### 2. React Hydration Warning
**Problem**: Warning about server-client mismatch for `class` and `data-js-focus-visible` attributes.

**Root Cause**:
- Focus-visible polyfill adds `data-js-focus-visible` attribute on client side
- Server-rendered HTML doesn't have this attribute
- Causes hydration mismatch

**Fix Applied**:
```tsx
// frontend/src/app/layout.tsx
<html lang="en" data-theme="dark" suppressHydrationWarning>
  <body className="..." suppressHydrationWarning>
```

**File Modified**: `frontend/src/app/layout.tsx`

---

## Important Notes

### Backend Status
- Phase-03 backend is configured and ready
- Database: Neon PostgreSQL (configured)
- OpenAI API Key: Configured
- JWT Authentication: Configured

### Recommended Next Steps

1. **Restart the frontend** to pick up the timeout change:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Start the Phase-03 backend** (if not running):
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Stop the Phase-02 backend** if it's still running:
   ```bash
   # Find the process
   ps aux | grep uvicorn
   # Kill the process (replace PID with actual process ID)
   kill <PID>
   ```

---

## Testing Checklist

- [ ] Frontend loads without hydration warnings
- [ ] Can send messages to chatbot without timeout
- [ ] Chatbot responds within 60 seconds
- [ ] OpenAI function calling works correctly
- [ ] Tasks can be created/listed/updated via chat

---

## Performance Optimization Suggestions (Future)

1. **Add Loading States**: Show progress indicators for long-running operations
2. **Implement Streaming**: Use OpenAI streaming API for faster perceived response
3. **Cache Responses**: Cache common queries to reduce API calls
4. **Optimize Prompts**: Reduce token usage to speed up responses
5. **Consider WebSockets**: For real-time bidirectional communication

---

## Files Modified
1. `/frontend/src/services/api.ts` - Increased timeout to 60 seconds
2. `/frontend/src/app/layout.tsx` - Added suppressHydrationWarning
