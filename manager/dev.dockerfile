FROM docker.io/python:3.11-slim

ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    redis-server \
    git && \
    pip install --upgrade pip && \
    pip install debugpy

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV SMB_MOUNT_POINT=/mnt/smb
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
