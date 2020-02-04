FROM python:2.7-alpine

MAINTAINER "lchuang@ninthdecimal.com"

RUN apk add build-base

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

EXPOSE 1999

CMD ["app/app.py"]