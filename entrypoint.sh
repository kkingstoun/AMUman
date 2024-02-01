#!/bin/bash
if [ "$1" = "manager" ]; then
    echo "Running the manager"

    python backend/manage.py makemigrations
    python backend/manage.py makemigrations common_models
    python backend/manage.py migrate
    python backend/manage.py migrate common_models
    python backend/manage.py migrate --settings=amuman.settings_manager
    python backend/manage.py migrate --settings=amuman.settings_node

    mkdir -p "$SMB_MOUNT_POINT"
    if mount -t cifs -o username="$SMB_USER",password="$SMB_PASSWORD",uid=1000,gid=1000 "$SMB_URL" "$SMB_MOUNT_POINT"; then
        echo "Mount success!"
        python backend/manage.py runserver 0.0.0.0:8000 --settings=amuman.settings_manager
    else
        echo "Mount failed!"
        exit 1
    fi

elif [ "$1" = "node" ]; then
    echo "Running the node"
    mkdir -p "$SMB_MOUNT_POINT"
    if mount -t cifs -o username="$SMB_USER",password="$SMB_PASSWORD",uid=1000,gid=1000 "$SMB_URL" "$SMB_MOUNT_POINT"; then
        echo "Mount success!"
        bash
    else
        echo "Mount failed!"
        exit 1
    fi

else
    exec "$@"
fi
