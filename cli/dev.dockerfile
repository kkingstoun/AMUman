FROM docker.io/python:3.11-slim

ARG DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git && \
    pip install --upgrade pip && \
    pip install debugpy

WORKDIR /app
COPY pyproject.toml .
RUN pip install . && pip uninstall -y amuman-cli
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD bash
