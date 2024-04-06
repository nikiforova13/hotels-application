from celery import Celery

# from celery.schedules import crontab
celery_app = Celery(
    "tasks_celery",
    broker="redis://localhost:6379",
    include=["app.tasks_celery.tasks" "app.tasks_celery.scheduled"],
)

celery_app.conf.beat_schedule = {
    "period": {
        "task": "periodic_task",
        "schedule": 5,  # 10 seconds
        # 'schedule': crontab(minute='30', hour='15') crontab
    }
}
