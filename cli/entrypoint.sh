#!/bin/bash

mkdir -p "$SMB_MOUNT_POINT"
if mount -t cifs -o username="$SMB_USER",password="$SMB_PASSWORD",uid=1000,gid=1000 "$SMB_URL" "$SMB_MOUNT_POINT"; then
    echo "Mount success!"
else
    echo "Mount failed!"
    exit 1
fi

pip install -e .
mkdir -p ~/.config/amuman
echo 'manager_url = "http://amuman-manager:8000"
shared_dir_root = "/nas"' > ~/.config/amuman/amuman.toml
amuman-cli --install-completion bash
source ~/.bash_completions/amuman-cli.sh
bash
