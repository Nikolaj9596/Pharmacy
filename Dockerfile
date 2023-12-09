FROM python:3.11-small

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1\
    POETRY_VERSION=1.5.1 \
    PATH="${PATH}:/usr/local/bin/python"\
    PATH="${PATH}:/root/.poetry/bin"\
    PATH="${PATH}:/app/src"

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-root --no-ansi -vvv --no-interaction



