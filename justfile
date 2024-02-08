run cmd arg="None": build
	sudo docker run --rm -it \
		--name amuman-{{cmd}} \
		--network amuman \
		--cap-add SYS_ADMIN \
		--cap-add DAC_READ_SEARCH \
		{{ if cmd == "node" { "--gpus all" } else { "" } }} \
		{{ if cmd == "manager" { "-p 8000:8000 -p 5678:5678" } else { "" } }} \
		--env-file ./.env \
		-v .:/app \
		amuman {{cmd}} {{arg}}

network:
	sudo docker network create amuman

build:
	sudo docker build . -t amuman

staging:
	podman build backend -f backend/dockerfile -t amuman-staging
	podman run --rm -it \
		--name amuman-staging \
		--network amuman-proxy \
		-e SECRET_KEY=qweert \
		-e SMB_MOUNT_POINT=/nas \
		-v /nas:/nas \
		amuman-staging

deploy:
	podman run --rm -it \
		--name amuman-staging \
		--network amuman-proxy \
		-v ./manager_config:/app \
		-v /nas:/shared \
		ghcr.io/kkingstoun/amuman:0.0.4