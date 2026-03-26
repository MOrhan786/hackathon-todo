from pydantic_settings import BaseSettings
from typing import Optional
import warnings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Required environment variables:
        - DATABASE_URL: PostgreSQL connection string
        - JWT_SECRET_KEY: Secret key for JWT access tokens
        - JWT_REFRESH_SECRET_KEY: Secret key for JWT refresh tokens
        - OPENAI_API_KEY: OpenAI API key for chatbot functionality
    
    Optional environment variables (have defaults):
        - ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
        - SERVER_HOST, SERVER_PORT, DEBUG
        - KAFKA_BOOTSTRAP_SERVERS, KAFKA_ENABLED
        - DAPR_ENABLED, DAPR_HTTP_PORT, DAPR_PUBSUB_NAME
    """
    
    # Database settings (Required)
    DATABASE_URL: str
    
    # JWT settings (Required)
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Server settings (Optional)
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False
    
    # OpenAI settings (Required for chatbot)
    OPENAI_API_KEY: str
    
    # Kafka settings (Optional)
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_ENABLED: bool = False
    
    # Dapr settings (Optional)
    DAPR_ENABLED: bool = False
    DAPR_HTTP_PORT: int = 3500
    DAPR_PUBSUB_NAME: str = "kafka-pubsub"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables
    
    def validate_secrets(self) -> None:
        """
        Validate that required secrets are properly configured.
        Raises ValueError if any required secrets are missing or use default values.
        """
        errors = []
        
        # Check DATABASE_URL
        if not self.DATABASE_URL or self.DATABASE_URL.startswith("postgresql://postgres:password"):
            errors.append("DATABASE_URL must be set to a valid PostgreSQL connection string")
        
        # Check JWT keys
        if not self.JWT_SECRET_KEY or self.JWT_SECRET_KEY.startswith("your-super-secret"):
            errors.append("JWT_SECRET_KEY must be set to a secure random value")
        
        if not self.JWT_REFRESH_SECRET_KEY or self.JWT_REFRESH_SECRET_KEY.startswith("your-super-secret"):
            errors.append("JWT_REFRESH_SECRET_KEY must be set to a secure random value")
        
        # Check OPENAI_API_KEY
        if not self.OPENAI_API_KEY or self.OPENAI_API_KEY.startswith("sk-your"):
            errors.append("OPENAI_API_KEY must be set to a valid OpenAI API key")
        
        if errors:
            raise ValueError("\n".join(errors))


# Create a single instance of settings
settings = Settings()

# Validate secrets on import (only in non-test environments)
import os
if os.getenv("PYTEST_CURRENT_TEST") is None:
    try:
        settings.validate_secrets()
    except ValueError as e:
        warnings.warn(
            f"\n⚠️  Security Warning: Missing or insecure configuration!\n{e}\n\n"
            f"Please copy backend/.env.example to backend/.env and configure all required values.\n"
            f"See backend/.env.example for guidance.",
            UserWarning
        )