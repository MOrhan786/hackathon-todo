#!/usr/bin/env python
# simple_backend_server.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import using relative imports by temporarily adjusting sys.path
original_path = sys.path[:]
try:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

    from backend.routes import tasks
    from backend.core.config import settings
    from backend.core.db import create_db_and_tables
    from contextlib import asynccontextmanager
finally:
    sys.path[:] = original_path  # Restore original path

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for application startup and shutdown.
    Creates database tables on startup.
    """
    logger.info("Initializing database tables...")
    # Temporarily adjust path for this import
    original_path = sys.path[:]
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
        from backend.core.db import create_db_and_tables
        create_db_and_tables()
    finally:
        sys.path[:] = original_path

    logger.info("Database tables initialized successfully.")
    yield
    logger.info("Shutting down...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Phase II Todo API",
        description="Secure task management API with JWT authentication and user isolation",
        version="1.0.0",
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*", "Authorization"],  # Allow all headers plus Authorization for JWT
    )

    # Include routers
    # Adjust path for import
    original_path = sys.path[:]
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
        from backend.routes import tasks
        app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    finally:
        sys.path[:] = original_path

    @app.get("/health")
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}

    return app


# Create the application instance
app = create_app()


# Include this so the app can be run with uvicorn
if __name__ == "__main__":
    import uvicorn
    # Get settings from backend
    settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'core', 'config.py')
    if os.path.exists(settings_path):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
        from core.config import settings
        sys.path.pop(0)
    else:
        # Default settings if config not found
        class DefaultSettings:
            SERVER_HOST = "0.0.0.0"
            SERVER_PORT = 8000
        settings = DefaultSettings()

    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)