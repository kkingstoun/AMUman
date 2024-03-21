FROM docker.io/python:3.11-slim

ARG DEBIAN_FRONTEND="noninteractive"
ARG AMUMAX_VER=2024.02.21
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git && \
    pip install --upgrade pip && \
    pip install debugpy

# amumax
RUN curl -Ls https://github.com/MathieuMoalic/amumax/releases/download/${AMUMAX_VER}/amumax > /bin/amumax && \
    curl -Ls https://github.com/MathieuMoalic/amumax/releases/download/${AMUMAX_VER}/libcufft.so.10 > /bin/libcufft.so.10 && \
    curl -Ls https://github.com/MathieuMoalic/amumax/releases/download/${AMUMAX_VER}/libcurand.so.10 > /bin/libcurand.so.10 && \
    chmod +x /bin/amumax
    
WORKDIR /app
COPY pyproject.toml .
RUN pip install . && pip uninstall -y amuman-node
ENV SMB_MOUNT_POINT=/mnt/smb
COPY ./dev.entrypoint.sh /dev.entrypoint.sh
ENTRYPOINT ["/dev.entrypoint.sh"]
