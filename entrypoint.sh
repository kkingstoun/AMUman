#!/bin/bash

mkdir -p "$SMB_MOUNT_POINT"
if mount -t cifs -o username="$SMB_USER",password="$SMB_PASSWORD",uid=1000,gid=1000 "$SMB_URL" "$SMB_MOUNT_POINT"; then
    echo "Mount success!"
else
    echo "Mount failed!"
    exit 1
fi

if [ "$1" = "manager" ]; then
    echo "Running the manager"
    cd /app/backend
    rm -rfd *.sqlite3
    find . -type d -name "__pycache__" -exec rm -rdf {} +
    find . -type d -name "migrations" -exec rm -rdf {} +
    redis-server /etc/redis/redis.conf

    python manage.py makemigrations 
    python manage.py migrate 
    python manage.py makemigrations manager
    python manage.py migrate --settings=amuman.settings_manager

    if [ "$2" = "debug" ]; then
       python -m debugpy --listen 0.0.0.0:5678 --wait-for-client /app/backend/manage.py runserver 0.0.0.0:8000 --settings=amuman.settings_manager
    elif [ "$2" = "bash" ]; then
        bash
    else
        python manage.py runserver 0.0.0.0:8000 --settings=amuman.settings_manager
    fi

elif [ "$1" = "node" ]; then
    pip install -e /app/node
    export NODE_NAME=test_node 
    bash

elif [ "$1" = "cli" ]; then
    pip install -e /app/cli
    mkdir -p ~/.config/amuman
    echo 'manager_url = "http://amuman-manager:8000"
shared_dir_root = "/nas"' > ~/.config/amuman/amuman.toml
    amuman-cli --install-completion bash
    source ~/.bash_completions/amuman-cli.sh
    bash

else
    exec "$@"
fi
