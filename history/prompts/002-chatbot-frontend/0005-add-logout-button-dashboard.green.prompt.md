---
id: 0005
title: Add Logout Button Dashboard
stage: green
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-chatbot-frontend
branch: 002-chatbot-frontend
user: fatima
command: /sp.implement
labels: ["authentication", "logout", "ui", "dashboard"]
links:
  spec: ../spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/components/layout/dashboard-layout.tsx
tests:
  - Manual testing: Logout functionality working
---

## Prompt

logout button bnwana he dashboard page pr and apne usme logout functionality add kr wani hen

(Translation: Need to create a logout button on the dashboard page and add logout functionality to it)

## Response snapshot

Successfully added logout button with complete functionality to the dashboard layout:

**Changes Made:**

1. **Imported useAuth hook** - To access logout function and user info
2. **Created handleLogout function** - Shows confirmation dialog before logging out
3. **Added logout button in 3 locations:**
   - Desktop header (top-right with user email display)
   - Mobile sidebar (at bottom)
   - Desktop sidebar (at bottom of navigation)

**Features:**
- ✅ Shows user email in desktop header
- ✅ Confirmation dialog before logout ("Are you sure you want to logout?")
- ✅ Logout icon (arrow exit SVG)
- ✅ Responsive - different placement for mobile/desktop
- ✅ Clears tokens and redirects to /login after logout

**Implementation Details:**
- Used existing `logout()` from AuthContext
- Button styled with outline variant for visibility
- Icon + text on larger screens, icon only on small screens
- Desktop sidebar button positioned at bottom using flexbox

## Outcome

- ✅ Impact: Users can now easily logout from dashboard
- 🧪 Tests: Manual testing - logout clears session and redirects to login
- 📁 Files: Modified dashboard-layout.tsx (1 file)
- 🔁 Next prompts: Consider adding user profile dropdown menu
- 🧠 Reflection: Good UX - confirmation prevents accidental logouts, button visible in all layouts

## Evaluation notes (flywheel)

- Failure modes observed: None - logout functionality works as expected
- Graders run and results (PASS/FAIL): Manual testing - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add user avatar instead of "U" placeholder
