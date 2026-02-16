from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import tasks
from routes import chatbot
from routes import reminders
from routes.auth import router as auth_router
from routes.events import router as events_router
from core.config import settings
from core.db import create_db_and_tables
from core.kafka import close_kafka_producer
from contextlib import asynccontextmanager
import logging
from jose import JWTError


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for application startup and shutdown.

    Creates database tables on startup. Initializes Kafka producer if enabled.
    """
    logger.info("Initializing database tables...")
    create_db_and_tables()
    logger.info("Database tables initialized successfully.")

    if settings.KAFKA_ENABLED:
        logger.info("Kafka is enabled. Producer will connect lazily on first event.")

    yield

    logger.info("Shutting down...")
    await close_kafka_producer()


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Phase II Todo API",
        description="Secure task management API with JWT authentication and user isolation",
        version="1.0.0",
        debug=settings.DEBUG,
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
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    app.include_router(reminders.router, prefix="/api", tags=["reminders"])
    app.include_router(chatbot.router, tags=["chatbot"])
    app.include_router(auth_router, tags=["auth"])
    app.include_router(events_router, tags=["events"])

    # Global exception handlers for JWT and auth-related errors
    @app.exception_handler(JWTError)
    async def jwt_exception_handler(request: Request, exc: JWTError):
        """Handle JWT errors globally."""
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid authentication credentials"}
        )

    @app.get("/")
    def root():
      return {"message": "Backend is running"}

    @app.get("/health")
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}

    @app.get("/dapr/subscribe")
    def dapr_subscribe():
        """Dapr subscription discovery endpoint (must be at root level)."""
        if not settings.DAPR_ENABLED:
            return []
        return [
            {
                "pubsubname": settings.DAPR_PUBSUB_NAME,
                "topic": "task-events",
                "route": "/events/task-events",
            },
            {
                "pubsubname": settings.DAPR_PUBSUB_NAME,
                "topic": "reminders",
                "route": "/events/reminders",
            },
            {
                "pubsubname": settings.DAPR_PUBSUB_NAME,
                "topic": "task-updates",
                "route": "/events/task-updates",
            },
        ]

    return app


# Create the application instance
app = create_app()


# Include this so the app can be run with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)