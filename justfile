network:
	sudo docker network create amuman

build:
	sudo docker build . -t amuman

build_db:
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py manage.py makemigrations common_models    
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py manage.py migrate
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py makemigrations --settings=amuman.settings_manager
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py makemigrations --settings=amuman.settings_node
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py makemigrations --settings=amuman.settings_client
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py migrate --settings=amuman.settings_manager
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py migrate --settings=amuman.settings_node
	sudo docker run --rm -it -v .:/app amuman poetry run python backend/manage.py migrate --settings=amuman.settings_client

manager: 
	sudo docker rm -f manager
	sudo docker run --network amuman --rm -it -v .:/app --name manager -p 8000:8000 amuman

node:
	sudo docker rm -f node
	sudo docker run --network amuman --gpus all --rm -it -v .:/app --name node amuman poetry run python backend/manage.py runserver --settings=amuman.settings_node
it:
	sudo docker run --network amuman --gpus all --rm -it -v .:/app amuman bash
