# Todo Application Backend

This is the backend for the Phase 2 Todo Application, featuring authentication, database persistence, and secure API endpoints.

## Features

- **User Authentication**: JWT-based authentication with secure registration and login
- **Todo Management**: Full CRUD operations for todo items
- **User Isolation**: Users can only access their own todos
- **Database Persistence**: Neon PostgreSQL with SQLModel ORM
- **Security**: Password hashing, input validation, and authentication middleware

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLModel ORM with Neon PostgreSQL
- **Authentication**: JWT tokens with HS256 algorithm
- **Password Security**: bcrypt hashing
- **Environment**: Python 3.9+

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure environment variables**
   Copy the example environment file and update with your values:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your database URL and secret key
   ```

5. **Run the application**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout (placeholder)

### Todos
- `GET /todos` - Get user's todos (with optional filtering)
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

### Other
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /protected` - Example protected endpoint

## Security

- All endpoints except `/`, `/health`, and `/auth/*` require authentication
- JWT tokens are verified on each request
- Users can only access their own data
- Passwords are securely hashed using bcrypt
- Input validation is enforced via Pydantic schemas

## Database

The application uses SQLModel ORM with Neon PostgreSQL. The data models include:

- **User**: Stores user information with email and hashed password
- **Todo**: Stores todo items with title, description, completion status, and user association

## Development

To run in development mode with auto-reload:

```bash
cd backend
uvicorn main:app --reload
```

To run tests:
```bash
python -m pytest
```

## Environment Variables

- `SECRET_KEY`: Secret key for JWT signing (change in production!)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `DATABASE_URL`: Database connection string