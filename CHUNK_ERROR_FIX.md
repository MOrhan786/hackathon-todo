# Fix for ChunkLoadError

## 🔴 Error Message
```
ChunkLoadError: Loading chunk app/layout failed.
(timeout: http://localhost:3000/_next/static/chunks/app/layout.js)
```

## 🎯 What This Means

Next.js builds your app into "chunks" (JavaScript files). This error happens when:
- Browser tries to load an old chunk that no longer exists
- Build cache is corrupted
- Hot Module Replacement (HMR) got out of sync
- Network timeout loading chunk files

## ✅ Quick Fix (Automated)

Run this script to fix it automatically:

```bash
cd /mnt/d/main-hackathon-folder/hackathon2/phase-03-todo-list
./fix-chunk-error.sh
```

## 🔧 Manual Fix (Step-by-Step)

### Step 1: Stop Frontend
```bash
cd /mnt/d/main-hackathon-folder/hackathon2/phase-03-todo-list/frontend

# Stop the Next.js dev server
# Press Ctrl+C in the terminal running npm run dev
# OR kill the process:
pkill -f "next dev"
```

### Step 2: Clear All Caches
```bash
# Clear Next.js build cache
rm -rf .next

# Clear node modules cache
rm -rf node_modules/.cache

# Clear TypeScript cache
rm -rf tsconfig.tsbuildinfo
```

### Step 3: Restart Frontend
```bash
npm run dev
```

**Wait for the compilation to complete** - look for:
```
✓ Compiled successfully
```

### Step 4: Clear Browser Cache

**Option A: Hard Refresh**
- **Windows/Linux**: `Ctrl + Shift + R`
- **Mac**: `Cmd + Shift + R`

**Option B: Clear Browser Data (if hard refresh doesn't work)**
1. Open DevTools (F12)
2. Right-click the refresh button → "Empty Cache and Hard Reload"

**Option C: Clear all site data**
1. Open DevTools (F12)
2. Go to **Application** tab
3. Click **Clear site data**
4. Refresh the page

### Step 5: Test
Navigate to `http://localhost:3000` - it should load without errors.

## 🚨 If Error Persists

### 1. Nuclear Option - Full Clean
```bash
cd frontend

# Stop server
pkill -f "next dev"

# Remove everything
rm -rf .next node_modules/.cache tsconfig.tsbuildinfo

# Reinstall dependencies (only if needed)
# rm -rf node_modules package-lock.json
# npm install

# Restart
npm run dev
```

### 2. Check for Port Conflicts
```bash
# See what's running on port 3000
lsof -i:3000

# Kill it if needed
lsof -ti:3000 | xargs kill -9
```

### 3. Check Network Tab
1. Open DevTools → Network tab
2. Refresh the page
3. Look for failed chunk requests
4. Check if they're returning 404 or timing out

### 4. Disable Browser Extensions
Some extensions interfere with chunk loading:
- Ad blockers
- Privacy extensions
- Security extensions

Try in an incognito/private window.

## 🔍 Root Causes

This error typically happens after:
- ✏️ Editing `layout.tsx` (which we just did!)
- 🔄 Hot reload issues
- 💾 Build cache corruption
- 🌐 Network issues
- ⚡ Fast Save plugin in VSCode

## 🛡️ Prevention

### 1. Wait for Compilation
After saving files, wait for:
```
✓ Compiled /app/layout in XXXms
```

### 2. Disable Fast Refresh Temporarily
If you're making lots of changes, temporarily disable:

Add to `next.config.js`:
```javascript
module.exports = {
  reactStrictMode: true,
  // Disable fast refresh during heavy development
  // webpack: (config) => {
  //   config.watchOptions = {
  //     poll: 1000,
  //     aggregateTimeout: 300,
  //   }
  //   return config
  // }
}
```

### 3. Use Stable Node Version
```bash
node --version  # Should be v18.x or v20.x
```

## 📊 Success Checklist

After applying the fix, verify:
- [ ] Frontend compiles without errors
- [ ] Page loads at http://localhost:3000
- [ ] No ChunkLoadError in browser console
- [ ] No hydration warnings (should be suppressed)
- [ ] Can navigate between pages
- [ ] Hot reload works on file changes

## 🎯 Quick Commands Reference

```bash
# Stop frontend
pkill -f "next dev"

# Clear cache
rm -rf .next node_modules/.cache tsconfig.tsbuildinfo

# Restart
npm run dev

# Check port
lsof -i:3000

# Kill port
lsof -ti:3000 | xargs kill -9
```

## 💡 Pro Tips

1. **Always wait for compilation** before refreshing
2. **Use terminal logs** to see what Next.js is doing
3. **Clear browser cache** regularly during development
4. **Restart dev server** when layout/config files change
5. **Check `.next` folder size** - if > 500MB, clear it

## 🔗 Related Errors

This fix also resolves:
- `ChunkLoadError: Loading chunk failed`
- `Loading chunk [id] failed`
- `Timeout loading chunk`
- `Failed to fetch dynamically imported module`

---

**Still stuck?** Check the terminal running `npm run dev` for specific error messages.
