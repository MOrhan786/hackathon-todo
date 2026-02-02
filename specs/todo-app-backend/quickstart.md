# Quickstart Guide: Todo Application Backend

## Prerequisites

- Python 3.9+
- Neon PostgreSQL database account
- pip package manager

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlmodel python-jose[cryptography] passlib[bcrypt] psycopg2-binary python-dotenv
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Database Setup
```bash
# Run initial migration (when implemented)
python -c "from database.init_db import create_db_and_tables; create_db_and_tables()"
```

### 6. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

Once running, the API will be available at `http://localhost:8000`:

- Health check: `GET /health`
- Register: `POST /auth/register`
- Login: `POST /auth/login`
- Todos: `GET /todos`, `POST /todos`, `PUT /todos/{id}`, `DELETE /todos/{id}`

## Testing

To test the API:
1. Register a user: `POST /auth/register`
2. Login to get JWT token: `POST /auth/login`
3. Use the token to access todo endpoints with `Authorization: Bearer <token>`