FROM python:3.8-alpine3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app 

COPY requirements.txt .

RUN apk add --no-cache --update postgresql-libs \
  libffi-dev \
  libxml2 \ 
  libxslt-dev \
  && echo "********* ensure pip dependencies **********" \
  && pip3 install --no-cache --upgrade pip setuptools wheel \
  && apk add --no-cache --update --virtual .build-deps gcc musl-dev postgresql-dev \
  && pip install -r requirements.txt --no-cache-dir \
  && apk del --purge .build-deps \
  && rm -rf /var/cache/apk/*

COPY . /app

EXPOSE 8080

ENTRYPOINT ["python", "manage.py", "runserver", "0:8080"]

