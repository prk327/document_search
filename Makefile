build:
	DOCKER_BUILDKIT=1 docker build -f src/Dockerfile -t smartsearch:0.1 .

clear:
	docker image rm smartsearch:0.1