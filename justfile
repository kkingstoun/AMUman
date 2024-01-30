network:
	sudo docker network create amuman

build:
	sudo docker build . -t amuman

build_db:
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py manage.py makemigrations  
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py manage.py migrate 
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py manage.py makemigrations common_models    
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py manage.py migrate common_models    
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py makemigrations --settings=amuman.settings_manager
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py makemigrations --settings=amuman.settings_node
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py makemigrations --settings=amuman.settings_client
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py migrate --settings=amuman.settings_manager
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py migrate --settings=amuman.settings_node
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py migrate --settings=amuman.settings_client

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
