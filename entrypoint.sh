#!/bin/bash

# echo "Starting Initialization"
# poetry run python backend/manage.py makemigrations --settings=amuman.settings_manager
# poetry run python backend/manage.py makemigrations --settings=amuman.settings_node
# poetry run python backend/manage.py makemigrations --settings=amuman.settings_client
# poetry run python backend/manage.py migrate --settings=amuman.settings_manager
# poetry run python backend/manage.py migrate --settings=amuman.settings_node
# poetry run python backend/manage.py migrate --settings=amuman.settings_client
mkdir $SMB_MOUNT_POINT
mount -t cifs -o username=$SMB_USER,password=$SMB_PASSWORD,uid=1000,gid=1000 $SMB_ADDRESS $SMB_MOUNT_POINT
ls /zfn
exec "$@"
