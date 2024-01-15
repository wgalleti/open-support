FROM python:3.12.0-alpine3.18
RUN \
  apk update && \
  apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT 1

# install dependencies
COPY Pipfile Pipfile.lock ./

# install pipenv on the container
RUN pip install -U pipenv

# install project dependencies
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app/