# Quick Fix Guide - Chat Timeout Error

## 🔴 Problem
You were getting these errors:
1. ❌ `AxiosError: timeout of 10000ms exceeded` when sending chat messages
2. ⚠️ Hydration warning: `Extra attributes from the server: class,data-js-focus-visible`

## ✅ Solution Applied

### Automated Fix (Recommended)
Just run this command to restart everything with the fixes:

```bash
cd /mnt/d/main-hackathon-folder/hackathon2/phase-03-todo-list
./restart-services.sh
```

This will:
- Stop old backend and frontend processes
- Start Phase-03 backend on port 8000
- Start Phase-03 frontend on port 3000
- Apply all fixes automatically

### Manual Fix (If script doesn't work)

#### 1. Stop Old Processes
```bash
# Stop phase-02 backend
pkill -f "phase-02.*uvicorn"

# Stop frontend
pkill -f "next dev"

# Or kill by port
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

#### 2. Start Phase-03 Backend
```bash
cd /mnt/d/main-hackathon-folder/hackathon2/phase-03-todo-list/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Keep this terminal open or run in background with:
```bash
nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
```

#### 3. Restart Frontend (New Terminal)
```bash
cd /mnt/d/main-hackathon-folder/hackathon2/phase-03-todo-list/frontend
npm run dev
```

## 🔧 What Was Fixed

### 1. Timeout Error - FIXED ✅
**Changed**: `frontend/src/services/api.ts`
```typescript
// Before
timeout: 10000,  // 10 seconds - TOO SHORT!

// After
timeout: 60000,  // 60 seconds - Accommodates OpenAI API calls
```

**Why**: The chatbot makes 2 OpenAI API calls per message (one for tool detection, one for response), which can take 20-30 seconds total.

### 2. Hydration Warning - FIXED ✅
**Changed**: `frontend/src/app/layout.tsx`
```tsx
// Added suppressHydrationWarning to html and body tags
<html lang="en" data-theme="dark" suppressHydrationWarning>
  <body className="..." suppressHydrationWarning>
```

**Why**: Focus-visible polyfill adds attributes on client-side that don't match server HTML.

## 🧪 Testing

After restarting, test these:

1. **Frontend loads**: http://localhost:3000
2. **Backend health**: http://localhost:8000/health
3. **API docs**: http://localhost:8000/docs
4. **Send a chat message** - should respond within 60 seconds
5. **No hydration warnings** in browser console

## 📊 Expected Behavior

### ✅ Good Signs
- Chat messages send without timeout errors
- Responses arrive within 60 seconds
- No hydration warnings in console
- React DevTools suggestion is normal (not an error)

### ⚠️ Still Having Issues?

If you still see errors:

1. **Check OpenAI API Key**:
   - Make sure `OPENAI_API_KEY` in `backend/.env` is valid
   - Check quota at https://platform.openai.com/account/billing

2. **Check Database Connection**:
   - Verify `DATABASE_URL` in `backend/.env` is correct
   - Test connection: `psql $DATABASE_URL`

3. **Check Logs**:
   ```bash
   # Backend logs
   tail -f backend/backend.log

   # Frontend logs (in terminal running npm run dev)
   ```

## 🚀 Performance Tips

For faster chat responses in the future:

1. **Use GPT-3.5-turbo** instead of GPT-4 (faster, cheaper)
   - Change in `backend/services/chatbot_service.py:121`
   - `model="gpt-3.5-turbo"`

2. **Add loading indicators** to show progress

3. **Implement streaming** for real-time responses

## 📝 Files Modified

1. ✏️ `frontend/src/services/api.ts` (timeout: 10000 → 60000)
2. ✏️ `frontend/src/app/layout.tsx` (added suppressHydrationWarning)
3. ➕ `FIXES_APPLIED.md` (detailed documentation)
4. ➕ `restart-services.sh` (automated restart script)
5. ➕ `QUICK_FIX_GUIDE.md` (this file)

---

**Need Help?** Check `FIXES_APPLIED.md` for detailed technical information.
