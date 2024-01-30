#!/bin/bash

echo "Starting Initialization"
poetry run python backend/manage.py makemigrations --settings=amuman.settings_manager
poetry run python backend/manage.py makemigrations --settings=amuman.settings_node
poetry run python backend/manage.py makemigrations --settings=amuman.settings_client
poetry run python backend/manage.py migrate --settings=amuman.settings_manager
poetry run python backend/manage.py migrate --settings=amuman.settings_node
poetry run python backend/manage.py migrate --settings=amuman.settings_client

exec "$@"
