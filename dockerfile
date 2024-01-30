FROM nvidia/cuda:12.1.0-base-ubuntu22.04

ARG DEBIAN_FRONTEND="noninteractive"
ARG PYTHON_VER=3.10
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    bash-completion \
    ca-certificates \
    curl \
    git \
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

RUN useradd -m -u 1000 -s /bin/bash amuman_user
USER amuman_user
ENV PATH="/localbin:${PATH}"
ENV PATH="/usr/local/bin:${PATH}"
ENV PATH="/home/amuman_user/.local/bin:${PATH}"

RUN pip install --user poetry 
WORKDIR /app
ADD pyproject.toml poetry.lock /app/
RUN poetry install --no-root 
COPY . /app

CMD poetry run python backend/manage.py runserver 0.0.0.0:8000 --settings=amuman.settings_manager
