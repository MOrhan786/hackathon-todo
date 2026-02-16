# Notification consumer Dockerfile
# Minimal image — only needs aiokafka, no backend dependencies
FROM python:3.12-slim

WORKDIR /app

# Install only what the consumer needs
RUN pip install --no-cache-dir aiokafka

# Copy only the consumer code
COPY backend/consumers/notification_consumer.py ./notification_consumer.py

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "notification_consumer.py"]
