#!/bin/bash

echo "Running the manager"
rm -rfd *.sqlite3
find . -type d -name "__pycache__" -exec rm -rdf {} +
find . -type d -name "migrations" -exec rm -rdf {} +
redis-server /etc/redis/redis.conf

export SECRET_KEY=secret
./manage.py makemigrations manager
./manage.py migrate manager
./manage.py makemigrations 
./manage.py migrate 
export DJANGO_SUPERUSER_EMAIL=admin@pm.me 
export DJANGO_SUPERUSER_USERNAME=admin 
export DJANGO_SUPERUSER_PASSWORD=admin
./manage.py createsuperuser --noinput
./manage.py spectacular --validate --color --file schema.yml

amuman-manager() {
    ./manage.py runserver 0.0.0.0:8000
}
export -f amuman-manager
if [ "$1" = "debug" ]; then
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client manage.py runserver 0.0.0.0:8000
elif [ "$1" = "bash" ]; then
    bash
else
    ./manage.py runserver 0.0.0.0:8000
fi
