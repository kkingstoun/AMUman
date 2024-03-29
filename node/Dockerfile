FROM docker.io/python:3.11-slim

ARG DEBIAN_FRONTEND="noninteractive"
ARG AMUMAX_VER=2024.02.21
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    cifs-utils && \
    pip install --upgrade pip && \
    pip install debugpy

# amumax
RUN curl -Ls https://github.com/MathieuMoalic/amumax/releases/download/${AMUMAX_VER}/amumax > /bin/amumax && \
    curl -Ls https://github.com/MathieuMoalic/amumax/releases/download/${AMUMAX_VER}/libcufft.so.10 > /bin/libcufft.so.10 && \
    curl -Ls https://github.com/MathieuMoalic/amumax/releases/download/${AMUMAX_VER}/libcurand.so.10 > /bin/libcurand.so.10 && \
    chmod +x /bin/amumax
    
WORKDIR /app
COPY pyproject.toml .
RUN pip install .

COPY . .
RUN pip install .
ENV SMB_MOUNT_POINT=/shared

CMD mount --mkdir -t cifs -o username="$SMB_USER",password="$SMB_PASSWORD",uid=1000,gid=1000 "$SMB_URL" "$SMB_MOUNT_POINT" && amuman-node