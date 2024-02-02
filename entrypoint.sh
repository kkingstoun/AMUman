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
    cd /app
    rm /app/backend/*.sqlite3
    pip install -r /app/requirements.txt
    python backend/manage.py makemigrations 
    python backend/manage.py makemigrations common_models 
    python backend/manage.py migrate 
    python backend/manage.py migrate common_models 
    python backend/manage.py migrate --settings=amuman.settings_manager
    python backend/manage.py runserver 0.0.0.0:8000 --settings=amuman.settings_manager

elif [ "$1" = "node" ]; then
    pip install -e /app/node
    bash

elif [ "$1" = "cli" ]; then
    pip install -e /app/cli
    mkdir -p ~/.config/amuman
    echo 'manager_url = "http://manager:8000"
shared_dir_path = "/nas"' > ~/.config/amuman/amuman.toml
    amuman-cli --install-completion bash
    source ~/.bash_completions/amuman-cli.sh
    bash

else
    exec "$@"
fi
