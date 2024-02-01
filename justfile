network:
	sudo docker network create amuman

build:
	sudo docker build . -t amuman

manager: build
	sudo docker rm -f manager
	sudo docker run --rm -it \
		--name manager \
		--network amuman \
		--cap-add SYS_ADMIN \
		--cap-add DAC_READ_SEARCH \
		-p 8000:8000 \
		--env-file ./.env \
		amuman manager

node:
	docker run --rm -it \
		--name node \
		--network amuman \
		--env-file ./.env \
		-e NODE_NAME=test_node \
		-v ./node:/app \
		-w /app \
		docker.io/python:3.11-slim \
		/bin/sh -c "pip install -e . && bash"
it:
	sudo docker run --network amuman --gpus all --rm -it -v .:/app amuman bash

cli:
	sudo docker run --network amuman --rm -it -v ./cli:/app -w /app docker.io/python:3.11-slim /bin/sh -c "pip install -e . && bash"
