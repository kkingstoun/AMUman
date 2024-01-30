network:
	sudo docker network create amuman

build:
	sudo docker build . -t amuman

manager: build
	sudo docker rm -f manager
	sudo docker run --rm -it \
		--name manager \
		--network amuman \
		-p 8000:8000 \
		amuman

node: build
	sudo docker rm -f node
	sudo docker run --rm -it \
		--name node \
		--network amuman \
		--cap-add SYS_ADMIN \
		--cap-add DAC_READ_SEARCH \
		--gpus all \
		--env-file ./.env \
		amuman \
		ls

it:
	sudo docker run --network amuman --gpus all --rm -it -v .:/app amuman bash
