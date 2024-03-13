PYTHONPATH= PYTHONPATH=src

run:
	$(PYTHONPATH) uvicorn app.main:app --reload --port 8088 --host 127.0.0.1


init_migrate:
	alembic revision --autogenerate -m

migrate:
	alembic update head

downgrade:
	alembic downgrade -1