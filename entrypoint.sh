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
    cd /app/manager
    rm -rfd *.sqlite3
    find . -type d -name "__pycache__" -exec rm -rdf {} +
    find . -type d -name "migrations" -exec rm -rdf {} +
    redis-server /etc/redis/redis.conf

    python manage.py makemigrations 
    python manage.py migrate 

    if [ "$2" = "debug" ]; then
       python -m debugpy --listen 0.0.0.0:5678 --wait-for-client /app/manager/manage.py runserver 0.0.0.0:8000 
        python manage.py runserver 0.0.0.0:8000 
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
