set dotenv-load

proxy:     
    podman run -d --replace --tz local --pull newer \
        --name amuman-proxy-staging \
        --network amuman-staging \
        -v ./proxy/nginx.conf:/etc/nginx/conf.d/default.conf:z \
        docker.io/nginx:1.25.2-alpine3.18-slim

frontend:
    podman build ./frontend -t amuman-frontend-staging

    podman run -d --replace --tz local --pull newer \
        --name amuman-frontend-staging \
        --network amuman-staging \
        amuman-frontend-staging

redis:
    podman run -d --replace --tz local --pull newer \
        --name amuman-redis-staging \
        --network amuman-staging \
        docker.io/redis:7.2.4-alpine3.19

manager:
    podman build ./manager -t amuman-manager-staging

    podman run -d --replace --tz local --pull newer \
        --name amuman-manager-staging \
        --network amuman-staging \
        -v ./staging:/manager \
        -e SECRET_KEY=$SECRET_KEY \
        -e DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL \
        -e DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME \
        -e DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD \
        -e DOMAIN_URL=$DOMAIN_URL \
        amuman-manager-staging

node:
    podman build ./node -t amuman-node-staging

    podman run -d --replace --tz local --pull newer \
        --name amuman-node-staging \
        --network amuman-staging \
        -v ./mock_nas:/mnt/smb \
        -e DOMAIN_URL=$DOMAIN_URL \
        amuman-node-staging 

staging: frontend redis manager proxy