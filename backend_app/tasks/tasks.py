# darkhorse/backend_app/tasks.py
# This file would contain actual Celery tasks.
# It's included here to satisfy the `include=['backend_app.tasks']` in celery_worker.py
from .celery_worker import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="darkhorse.tasks.process_long_running_report")
def process_long_running_report(user_id: int, report_type: str):
    """
    Example of a long-running task that might generate a report.
    """
    logger.info(f"Starting long-running report generation for user {user_id}, type: {report_type}")
    import time
    time.sleep(10) # Simulate work
    # Logic to fetch data, process, generate report, store, and notify user
    logger.info(f"Finished long-running report generation for user {user_id}, type: {report_type}")
    return {"status": "completed", "report_url": f"/reports/{user_id}/{report_type}.pdf"}
