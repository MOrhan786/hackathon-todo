<<<<<<< HEAD
# Todo In-Memory Python Console App

A command-line and web-based Todo application that stores tasks only in memory using spec-driven development with Spec-Kit Plus and Qwen.

## Features

- Add task (with title and description)
- View/List all tasks with status indicators
- Update task details by ID
- Delete task by ID
- Mark task as complete/incomplete (toggle status)
- Web interface available at localhost:3000

## Requirements

- Python 3.13+
- UV package manager (for running the application)

## Usage

### Method 1: Using UV (full command)
```bash
uv run src/todo/__main__.py add --title "Buy groceries" --description "Milk, bread, eggs"
uv run src/todo/__main__.py list
uv run src/todo/__main__.py update --id 1 --title "Updated title"
uv run src/todo/__main__.py delete --id 1
uv run src/todo/__main__.py complete --id 1
```

### Method 2: Using the simplified command (recommended)
```bash
todo add --title "Buy groceries" --description "Milk, bread, eggs"
todo list
todo update --id 1 --title "Updated title"
todo delete --id 1
todo complete --id 1
```

The simplified `todo` command is available:
- On Windows as `todo.bat`
- On Unix-like systems as `todo.sh` (make sure to `chmod +x todo.sh` to make it executable)
- You can also add it to your PATH or create an alias for convenience

### Method 3: Using the Web Interface (NEW!)
1. Install dependencies: `pip install -r requirements.txt`
2. Start the web server: `python web_server.py` or use the scripts below
3. Open your browser and go to `http://localhost:3000`

#### Web Interface Scripts:
- On Windows: `start_web.bat`
- On Unix-like systems: `start_web.sh` (make sure to `chmod +x start_web.sh` to make it executable)

### Available Commands

#### CLI Commands:
- `add`: Add a new task
  - `--title`: Title of the task (required)
  - `--description`: Description of the task (required)

- `list`: List all tasks

- `update`: Update a task
  - `--id`: ID of the task to update (required)
  - `--title`: New title of the task (optional)
  - `--description`: New description of the task (optional)

- `delete`: Delete a task
  - `--id`: ID of the task to delete (required)

- `complete`: Toggle task completion status
  - `--id`: ID of the task to toggle (required)

## Project Structure

```
src/
└── todo/
    ├── __init__.py
    ├── __main__.py
    ├── models.py     # Task dataclass
    ├── storage.py    # In-memory operations
    └── cli.py        # Argparse interface
web_server.py         # Web server implementation
templates/            # HTML templates for web interface
└── index.html        # Main web page
requirements.txt      # Python dependencies
start_web.bat         # Windows script to start web server
start_web.sh          # Unix script to start web server
```

## Architecture

- **models.py**: Contains the Task dataclass with fields: id (int, auto-increment), title (str), description (str), completed (bool, default False), created_at (datetime)
- **storage.py**: Manages List[Task] with pure functions for all operations
- **cli.py**: Implements argparse subcommands for the user interface
- **web_server.py**: Flask web server that provides a web interface to the todo app
- **In-memory only**: No file or database persistence
=======
# Hackathon II – Phase 2: Frontend-Backend Integration

This project demonstrates the complete integration between the frontend and backend of a Todo application. The backend was developed in the `001-backend-api` phase and is now connected to the frontend with full authentication and authorization capabilities.

## 📋 Integration Summary

The frontend has been successfully integrated with the existing backend API to:

- Replace all mock data with real API calls
- Implement complete signup/signin flow
- Handle JWT tokens securely on the frontend
- Protect routes (public vs authenticated)
- Enable full CRUD operations for tasks
- Ensure Neon DB shows real User & Task records

## 🏗️ Architecture

### Backend API
- **Authentication**: `/auth/register`, `/auth/login`, `/auth/logout`
- **Tasks**: `/api/tasks` endpoints with full CRUD operations
- **Security**: JWT-based authentication with user isolation
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM

### Frontend Integration
- **Services**: `api-service.ts`, `task-service.tsx`, `auth-service.ts`
- **Routing**: Next.js middleware for route protection
- **State Management**: React Context for task operations
- **Security**: JWT token handling in localStorage

## 🚀 Getting Started

1. Start the backend server:
   ```bash
   cd backend
   uvicorn backend_server:app --reload
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Visit `http://localhost:3000` to access the application

## 📄 Documentation

- `INTEGRATION_PLAN.md` - Original integration plan
- `INTEGRATION_DOCUMENTATION.md` - Comprehensive integration documentation
- `INTEGRATION_VERIFICATION_PLAN.md` - Verification procedures
- `INTEGRATION_REPORT.md` - Final integration report
- `test_integration.sh` - Automated integration test script

## ✅ Features Implemented

- ✅ Real API calls (no mock data)
- ✅ Complete authentication flow
- ✅ Secure JWT handling
- ✅ Protected routes
- ✅ Full task CRUD operations
- ✅ User isolation
- ✅ Neon DB integration
>>>>>>> 4c9a8fb (Fix redirect after auth - dashboard now redirects to main todo app)
