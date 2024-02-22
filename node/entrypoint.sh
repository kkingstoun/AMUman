#!/bin/bash

mkdir -p "$SMB_MOUNT_POINT"
if mount -t cifs -o username="$SMB_USER",password="$SMB_PASSWORD",uid=1000,gid=1000 "$SMB_URL" "$SMB_MOUNT_POINT"; then
    echo "Mount success!"
else
    echo "Mount failed!"
    exit 1
fi

pip install -e .

if [ "$1" = "debug" ]; then
    python -m debugpy --listen 0.0.0.0:5679 --wait-for-client ./amuman_node/main.py
elif [ "$1" = "bash" ]; then
    bash
else
    exec bash
fi

