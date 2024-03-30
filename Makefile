PYTHONPATH= PYTHONPATH=src
APP = app/
run:
	$(PYTHONPATH) uvicorn app.main:app --reload --port 8088 --host 127.0.0.1

format:
	black $(APP)
	isort $(APP)

lint:
	flake8 $(APP)

rev:
	alembic revision --autogenerate -m

migrate:
	alembic update head

downgrade:
	alembic downgrade -1