build-image:
	sudo docker build -t stvoid/wtm:latest .

push-images:
	sudo docker image push stvoid/wtm:latest

docker-run:
	sudo docker run -d --name WTM -v ${PWD}/config.toml:/app/config.toml stvoid/wtm:latest
