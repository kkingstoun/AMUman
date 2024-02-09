#!/bin/bash

echo "Running the manager"
cd /app/backend
rm -rfd *.sqlite3
find . -type d -name "__pycache__" -exec rm -rdf {} +
find . -type d -name "migrations" -exec rm -rdf {} +
redis-server /etc/redis/redis.conf

python manage.py makemigrations 
python manage.py migrate 

export DJANGO_SUPERUSER_EMAIL=admin@pm.me 
export DJANGO_SUPERUSER_USERNAME=admin 
export DJANGO_SUPERUSER_PASSWORD=admin
python3 manage.py createsuperuser --noinput

if [ "$1" = "debug" ]; then
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client manage.py runserver 0.0.0.0:8000
elif [ "$1" = "bash" ]; then
    bash
else
    python manage.py runserver 0.0.0.0:8000
fi
