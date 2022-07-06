FROM python:3.9.12-slim-buster

ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

COPY ./requirements.txt $APP_HOME/

RUN pip install -r $APP_HOME/requirements.txt --no-cache-dir

COPY ./ $APP_HOME/
