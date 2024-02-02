network:
	sudo docker network create amuman

build:
	sudo docker build . -t amuman

manager: build
	sudo docker run --rm -it \
		--name manager \
		--network amuman \
		--cap-add SYS_ADMIN \
		--cap-add DAC_READ_SEARCH \
		-p 8000:8000 \
		--env-file ./.env \
		-v .:/app \
		amuman manager

node: build
	sudo docker run --rm -it \
		--name node \
		--network amuman \
		--env-file ./.env \
		--cap-add SYS_ADMIN \
		--cap-add DAC_READ_SEARCH \
		--gpus all \
		-e NODE_NAME=test_node \
		-v .:/app \
		amuman node

cli: build
	sudo docker run --rm -it \
		--name cli \
		--network amuman \
		--env-file ./.env \
		--cap-add SYS_ADMIN \
		--cap-add DAC_READ_SEARCH \
		-v .:/app \
		amuman cli
