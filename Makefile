APP = app/
ENV_FILE = app/.env
PROJECT_NAME = hotels-application


-include $(ENV_FILE)
run:
	poetry run uvicorn app.main:app --reload --port 8088 --host 127.0.0.1

celery_run:
	poetry run celery --app=app.tasks_celery.celery_config:celery_app worker -l INFO

format:
	black $(APP)
	isort $(APP)

lint:
	flake8 $(APP)

init_db:
	docker run -d --name $(DB_NAME) \
		-e POSTGRES_PASSWORD=$(DB_PASSWORD) \
		-e POSTGRES_DB=$(DB_NAME) \
		-e POSTGRES_USER=$(DB_USERNAME) \
		-p $(DB_PORT):5432 postgres:latest
	sleep 2
	alembic upgrade head

rev:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1