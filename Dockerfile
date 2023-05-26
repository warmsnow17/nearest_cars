FROM python:3.11-slim-buster

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /app


EXPOSE 8000

