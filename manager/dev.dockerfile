FROM docker.io/ubuntu:22.04

ARG DEBIAN_FRONTEND="noninteractive"
ARG PYTHON_VER=3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    bash-completion \
    ca-certificates \
    curl \
    git \
    cifs-utils \
    redis-server \
    python${PYTHON_VER} python${PYTHON_VER}-dev python3-pip python-is-python3 && \
    pip install --upgrade pip && \
    pip install debugpy

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV SMB_MOUNT_POINT=/mnt/smb
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
