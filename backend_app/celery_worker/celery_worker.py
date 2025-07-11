import os
import logging
from celery import Celery

# Configure basic logging for the Celery worker
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the Redis connection URLs from environment variables
broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Initialize the Celery application instance
celery_app = Celery(
    "gpn_tasks",
    broker=broker_url,
    backend=result_backend,
    include=['backend_app.tasks'] # Tells Celery to look for tasks in the 'tasks.py' file
)

# Optional configuration for production environments
celery_app.conf.update(
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    timezone='UTC',
    enable_utc=True,
)