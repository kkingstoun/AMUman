set dotenv-load

proxy:     
    podman run --rm -it --replace --tz local --pull newer \
        --name amuman-proxy-staging \
        --network amuman-staging \
        -v ./proxy/nginx.conf:/etc/nginx/conf.d/default.conf:z \
        docker.io/nginx:1.25.2-alpine3.18-slim

frontend:
    podman build ./frontend -t amuman-frontend-staging

    podman run --rm -it --replace --tz local --pull newer \
        --name amuman-frontend-staging \
        --network amuman-staging \
        amuman-frontend-staging

redis:
    podman run --rm -it --replace --tz local --pull newer \
        --name amuman-redis-staging \
        --network amuman-staging \
        docker.io/redis:7.2.4-alpine3.19

manager:
    podman build ./manager -t amuman-manager-staging

    podman run --rm -it --replace --tz local --pull newer \
        --name amuman-manager-staging \
        --network amuman-staging \
        -v ./staging:/manager \
        -e SECRET_KEY=$SECRET_KEY \
        -e DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL \
        -e DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME \
        -e DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD \
        -e DOMAIN=$DOMAIN \
        -e REDIS_HOST=amuman-redis-staging \
        amuman-manager-staging

node:
    podman build ./node -t amuman-node-staging

    podman run --rm -it --replace --tz local --pull newer \
        --name amuman-node-staging \
        --device=nvidia.com/gpu=all \
        -v ./mock_nas:/mnt/smb \
        -e MANAGER_DOMAIN=$DOMAIN \
        -e NODE_NAME=staging-node-1  \
        amuman-node-staging 

staging: frontend redis manager proxy

kill-staging:
    podman rm -f amuman-proxy-staging
    podman rm -f amuman-frontend-staging
    podman rm -f amuman-redis-staging
    podman rm -f amuman-manager-staging
    podman rm -f amuman-node-staging

prod version="0.0.7":
    podman run -d --replace --tz local --pull newer \
        --name amuman-frontend-prod \
        --network amuman-prod \
        ghcr.io/kkingstoun/amuman/frontend:{{version}}

    podman run -d --replace --tz local --pull newer \
        --name amuman-redis-prod \
        --network amuman-prod \
        docker.io/redis:7.2.4-alpine3.19

    podman run -d --replace --tz local --pull newer \
        --name amuman-manager-prod \
        --network amuman-prod \
        -v ./prod:/manager \
        -e SECRET_KEY=$SECRET_KEY \
        -e DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL \
        -e DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME \
        -e DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD \
        -e DOMAIN=$DOMAIN \
        -e REDIS_HOST=amuman-redis-prod \
        ghcr.io/kkingstoun/amuman/manager:{{version}}

    mkdir -p ./proxy
    curl -Ls https://raw.githubusercontent.com/kkingstoun/AMUman/v{{version}}/proxy/nginx.conf -o ./proxy/nginx.conf
    podman run -d --replace --tz local --pull newer \
        --name amuman-proxy-prod \
        --network amuman-prod \
        -v ./proxy/nginx.conf:/etc/nginx/conf.d/default.conf:z \
        docker.io/nginx:1.25.2-alpine3.18-slim

