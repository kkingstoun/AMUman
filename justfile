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

node: build
	sudo docker rm -f node
	sudo docker run --rm -it \
		--name node \
		--network amuman \
		--cap-add SYS_ADMIN \
		--cap-add DAC_READ_SEARCH \
		--gpus all \
		--env-file ./.env \
		-e NODE_ID=1 \
		amuman node
it:
	sudo docker run --network amuman --gpus all --rm -it -v .:/app amuman bash
