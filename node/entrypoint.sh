#!/bin/bash

set -e

if [ -z "$MANAGER_URL" ]; then
  echo "MANAGER_URL is not set"
  exit 1
fi
if [ -z "$NODE_NAME" ]; then
  echo "NODE_NAME is not set"
  exit 1
fi
if [ -z "$NODE_PASSWORD" ]; then
  echo "NODE_PASSWORD is not set"
  exit 1
fi

echo "Starting server"
amuman-node