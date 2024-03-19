set dotenv-load

staging:
	podman network create --ignore amuman-staging
	podman build . -t amuman-staging
	podman run --rm -it --replace --tz local --pull newer \
		--name amuman-staging \
		--network amuman-staging \
		-p 12502:12502 \
		-v ./staging:/manager \
		-e SECRET_KEY=$SECRET_KEY \
		-e DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL \
		-e DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME \
		-e DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD \
		-e DOMAIN_URL=$DOMAIN_URL \
		amuman-staging 