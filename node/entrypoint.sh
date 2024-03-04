#!/bin/bash

pip install -e .

if [ "$1" = "debug" ]; then
    python -m debugpy --listen 0.0.0.0:5679 --wait-for-client ./amuman_node/main.py
elif [ "$1" = "bash" ]; then
    bash
else
    exec bash
fi

