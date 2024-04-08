APP = app/

run:
	poetry run uvicorn app.main:app --reload --port 8088 --host 127.0.0.1

format:
	black $(APP)
	isort $(APP)

lint:
	flake8 $(APP)

rev:
	poetry run alembic revision --autogenerate -m

migrate:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1