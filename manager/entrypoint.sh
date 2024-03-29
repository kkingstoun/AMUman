#!/bin/bash

if [ -z "$SECRET_KEY" ]; then
  echo "SECRET_KEY is not set"
    exit 1
fi
if [ -z "$DJANGO_SUPERUSER_EMAIL" ]; then
  echo "DJANGO_SUPERUSER_EMAIL is not set"
    exit 1
fi
if [ -z "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "DJANGO_SUPERUSER_USERNAME is not set"
    exit 1
fi
if [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "DJANGO_SUPERUSER_PASSWORD is not set"
    exit 1
fi
if [ -z "$DOMAIN" ]; then
  echo "DOMAIN is not set"
    exit 1
fi

# if /config/db.sqlite3 does not exist, init the database
if [ ! -f /config/db.sqlite3 ]; then
  ./manage.py migrate
  ./manage.py createsuperuser --noinput
else
  ./manage.py migrate
fi
./manage.py collectstatic --noinput

./manage.py runserver 0.0.0.0:8000