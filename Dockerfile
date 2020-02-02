FROM python:2.7-alpine

MAINTAINER "lchuang@ninthdecimal.com"

RUN apk add build-base

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD [ "app.py" ]