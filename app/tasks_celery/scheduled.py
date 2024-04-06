from app.tasks_celery.celery_config import celery_app


@celery_app.task(name="periodic_task")
def periodict_task():
    print(12345)
