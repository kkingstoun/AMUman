FROM nvidia/cuda:12.3.1-base-ubuntu22.04

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
    pip install --upgrade pip &&\
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# amumax
RUN curl -Ls https://github.com/mathieumoalic/amumax/releases/latest/download/amumax > /bin/amumax && \
    curl -Ls https://github.com/mathieumoalic/amumax/releases/latest/download/libcufft.so.10 > /bin/libcufft.so.10 && \
    curl -Ls https://github.com/mathieumoalic/amumax/releases/latest/download/libcurand.so.10 > /bin/libcurand.so.10 && \
    chmod +x /bin/amumax

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install debugpy
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD bash
