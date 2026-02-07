# Phase 3 Quick Start Guide

## Prerequisites
- Python 3.12+ with venv
- Node.js 18+ with npm
- PostgreSQL database (Neon recommended)
- OpenAI API key

## Environment Setup

### 1. Backend Environment Variables

Ensure `/backend/.env` contains:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-here
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI (NEW for Phase 3)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False
```

### 2. Install Dependencies

**Backend**:
```bash
cd backend
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install
```

## Database Setup

The database tables will be created automatically on first run. To verify:

```bash
cd backend
source venv/bin/activate
python test_setup.py
```

Expected output:
```
✅ PASS - Database Setup
✅ PASS - Tools Import
✅ PASS - Services Import
🎉 All tests passed! Phase 3 implementation is ready.
```

## Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:3000

## Testing the AI Chat Interface

1. Open browser: http://localhost:3000
2. Navigate to the Chat interface
3. Try these commands:

### Create Tasks
```
"Create a task to buy groceries tomorrow"
"Add a high priority task to finish the report by Friday"
"Remind me to call mom"
```

### List Tasks
```
"Show my tasks"
"List pending tasks"
"What are my high priority tasks?"
```

### Update Tasks
```
"Change the grocery task to urgent priority"
"Update the report task to completed"
"Mark the first task as done"
```

### Complete Tasks
```
"Mark the grocery task as completed"
"I finished the report"
"Complete the first task"
```

### Delete Tasks
```
"Delete the grocery task"
"Remove the first task"
```

### Multi-Turn Conversations
The AI maintains context across messages:
```
You: "Create a task to buy milk"
AI: "Task created!"
You: "Make it high priority"  ← AI knows which task
AI: "Updated to high priority"
You: "Mark it as done"  ← AI still remembers
AI: "Task completed!"
```

### New Conversation
Click the "New Conversation" button to start fresh without previous context.

## API Endpoints

### Chat Endpoint
```bash
POST /api/chat/message
Authorization: Bearer <jwt_token>

Request:
{
  "message": "Create a task to buy groceries",
  "conversation_id": "optional-uuid-for-context"
}

Response:
{
  "message": "I've created a task titled 'Buy groceries'",
  "conversation_id": "uuid-for-tracking",
  "timestamp": "2026-02-06T12:00:00Z"
}
```

### Existing Task Endpoints (Unchanged)
All Phase 2 endpoints still work:
- `GET /api/tasks` - List tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

## Troubleshooting

### Backend won't start
1. Check `.env` file exists and has all required variables
2. Verify OpenAI API key is valid
3. Check database connection string
4. Run: `python test_setup.py` to diagnose issues

### Frontend errors
1. Check backend is running on port 8000
2. Verify JWT token is valid (try logging in again)
3. Check browser console for error messages

### Chat not responding
1. Verify `OPENAI_API_KEY` is set in backend `.env`
2. Check OpenAI API key has credits available
3. Check backend logs for OpenAI API errors

### "Conversation not found" error
This is normal when conversation_id from a previous session is used after database reset. Click "New Conversation" to start fresh.

## Architecture Overview

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
└────────┬────────┘
         │ HTTP + JWT
         ▼
┌─────────────────┐
│   FastAPI       │
│   Backend       │
├─────────────────┤
│ ChatbotService  │──► OpenAI GPT-4
│ TaskToolExecutor│
└────────┬────────┘
         │ SQL
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   (Neon)        │
├─────────────────┤
│ • conversations │
│ • messages      │
│ • tasks         │
│ • users         │
└─────────────────┘
```

## Features Implemented

✅ Natural language task creation
✅ Conversation persistence across requests
✅ Multi-turn context awareness
✅ 5 task management tools (add, list, complete, update, delete)
✅ User isolation (conversations belong to users)
✅ JWT authentication
✅ Stateless API design
✅ Error handling and logging
✅ Custom React chat UI

## Next Steps

- Read `PHASE3_IMPLEMENTATION.md` for detailed technical documentation
- Review `/backend/tools/task_tools.py` to understand tool definitions
- Check `/backend/services/chatbot_service.py` for OpenAI integration
- Explore `/backend/models/` for database schema

## Support

For issues or questions:
1. Check `PHASE3_IMPLEMENTATION.md` for detailed documentation
2. Run `python test_setup.py` to verify setup
3. Check backend logs for error messages
4. Review OpenAI API usage and rate limits

---

**Enjoy your AI-powered task management assistant! 🎉**
