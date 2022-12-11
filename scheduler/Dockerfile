FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml /app 
COPY README.md /app

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./scheduler /app/scheduler

ENV PYTHONPATH=/app

CMD ["python", "./scheduler/main.py"]
