FROM nvidia/cuda:12.1.0-base-ubuntu22.04

ARG DEBIAN_FRONTEND="noninteractive"
ARG PYTHON_VER=3.10
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    bash-completion \
    ca-certificates \
    curl \
    git \
    cifs-utils \
    python${PYTHON_VER} python${PYTHON_VER}-dev python3-pip python-is-python3 && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# amumax
RUN mkdir /localbin && cd /localbin && \
    curl -Ls https://github.com/mathieumoalic/amumax/releases/latest/download/amumax > amumax && \
    curl -Ls https://github.com/mathieumoalic/amumax/releases/latest/download/libcufft.so.10 > libcufft.so.10 && \
    curl -Ls https://github.com/mathieumoalic/amumax/releases/latest/download/libcurand.so.10 > libcurand.so.10 && \
    chmod +x amumax

# Add /localbin to PATH
ENV PATH="/localbin:${PATH}"

WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
CMD manager
