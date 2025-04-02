from celery import Celery

# Use Railway Redis URL
redis_url = "redis://:<your_redis_password>@<your_redis_host>:<your_redis_port>/0"

app = Celery(
    "server",
    broker=redis_url,
    backend=redis_url  # ✅ Change this line
)

# Celery Configuration
app.conf.update(
    result_backend=redis_url,  # ✅ Change from CELERY_RESULT_BACKEND
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True
)
