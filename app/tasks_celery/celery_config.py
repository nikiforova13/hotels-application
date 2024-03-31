from celery import Celery

celery_app = Celery(
    "tasks_celery", broker="redis://localhost:6379", include=["app.tasks_celery.tasks"]
)
