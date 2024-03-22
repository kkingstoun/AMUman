FROM docker.io/python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN mkdir -p /manager

ENV DEBUG=FALSE

ENTRYPOINT ["/app/entrypoint.sh"]
