build-image:
	sudo docker build -t stvoid/wtm:latest .
push-images:
	sudo docker image push stvoid/wtm:latest
docker-run:
	sudo docker run -d --name WTM -v ${PWD}/config.toml:/app/config.toml stvoid/wtm:latest

run.backend:
	cd src/backend && .venv/bin/python main.py
run.frontend:
	cd src/frontend/ && pnpm run dev

install.backend.requirements:
	cd src/backend && python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
install.frontend.dependencies:
	cd src/frontend/ && pnpm install

build.frontend:
	pnpm run ts-lint && pnpm run build
