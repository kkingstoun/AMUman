#!/bin/bash

set -e

if [ -z "$MANAGER_DOMAIN" ]; then
  echo "MANAGER_DOMAIN is not set"
    exit 1
fi
if [ -z "$NODE_NAME" ]; then
  echo "if [ -z "$NODE_NAME" ]; then
 is not set"
    exit 1
fi

echo "Starting server"
amuman-node