FROM python:3.11

ENV VENV_PATH="/opt/app/.venv"

WORKDIR /opt/app

RUN apt-get update && pip install "poetry==1.5.1" && poetry config virtualenvs.create false && python -m venv $VENV_PATH

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-cache

COPY . .

CMD ["uvicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.worker.UvicornWorker", "--port", "8000", "--host", "0.0.0.0"]