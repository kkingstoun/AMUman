FROM docker.io/python:3.11-slim

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get install -y --no-install-recommends \
    redis-server \
    nodejs \
    npm \
    caddy \
    git && \
    pip install --upgrade pip

WORKDIR /app/manager
COPY manager/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app/frontend
COPY frontend .
RUN npm install && npm run build

RUN echo "${DOMAIN_URL} localhost:12502 {\n\
	handle /api* {\n\
		reverse_proxy localhost:8000\n\
	}\n\
	handle {\n\
		reverse_proxy localhost:3000\n\
	}\n\
}" > /etc/caddy/Caddyfile

WORKDIR /app
COPY manager manager
RUN mkdir -p /manager

ENV SECRET_KEY=
ENV DJANGO_SUPERUSER_EMAIL=
ENV DJANGO_SUPERUSER_USERNAME=
ENV DJANGO_SUPERUSER_PASSWORD=
ENV DOMAIN_URL=
ENV DEBUG=FALSE

CMD redis-server /etc/redis/redis.conf \
    && ./manager/manage.py makemigrations manager \
    && ./manager/manage.py migrate manager \ 
    && ./manager/manage.py makemigrations \
    && ./manager/manage.py migrate \
    && ./manager/manage.py createsuperuser --noinput \
    && ./manager/manage.py runserver 0.0.0.0:8000 &\
    node /app/frontend/build&\
    caddy run --config /etc/caddy/Caddyfile
