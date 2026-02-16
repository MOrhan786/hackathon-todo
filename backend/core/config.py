from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    DATABASE_URL: str

    # JWT settings
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour as per spec
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Server settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False

    # OpenAI settings
    OPENAI_API_KEY: str

    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_ENABLED: bool = False

    # Dapr settings
    DAPR_ENABLED: bool = False
    DAPR_HTTP_PORT: int = 3500
    DAPR_PUBSUB_NAME: str = "kafka-pubsub"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a single instance of settings
settings = Settings()