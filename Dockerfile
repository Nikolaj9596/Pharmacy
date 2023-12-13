FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1\
    POETRY_VERSION=1.5.1 
    # PATH="${PATH}:/usr/local/bin/python"\
    # PATH="${PATH}:/root/.poetry/bin"

WORKDIR /app

ADD . /app/

RUN pip install --upgrade pip\
&& pip install "poetry==$POETRY_VERSION" \
&& poetry config virtualenvs.create false\
&& poetry export --without-hashes -f requirements.txt > requirements.txt\
&& sed -e "s/Skipping virtualenv creation, as specified in config file.//g" -i requirements.txt\
&& pip install -r requirements.txt --no-cache


