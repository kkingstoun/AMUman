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
