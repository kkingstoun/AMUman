#!/bin/bash

pip install -e .
mkdir -p ~/.config/amuman
echo 'manager_url = "http://amuman-manager-dev:8000"
shared_dir_root = "/mnt/smb"' > ~/.config/amuman/amuman.toml
amuman-cli --install-completion bash
source ~/.bash_completions/amuman-cli.sh
bash
