# build vue frontend static files
FROM node:18-alpine AS frontend
WORKDIR /frontend
RUN npm install -g pnpm
COPY src/frontend/package.json \
    src/frontend/pnpm-lock.yaml \
    src/frontend/vite.config.ts \
    src/frontend/index.html \
    src/frontend/tsconfig.json \
    src/frontend/.eslintrc.json ./
RUN pnpm install
COPY src/frontend/src src
COPY src/frontend/public public
RUN NODE_OPTIONS='--max-old-space-size=448' NODE_ENV=production pnpm build

FROM python:3.11-slim-buster as aiohttp-backend
WORKDIR /app
RUN cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" >/etc/timezone
RUN apt-get update && apt-get upgrade -y && apt-get install ca-certificates build-essential libmagic-dev -y && apt-get clean
RUN update-ca-certificates
COPY src/backend/requirements.txt .
RUN pip --no-cache-dir install -U pip setuptools && pip --no-cache-dir install -r requirements.txt
COPY --from=frontend frontend/dist ./static
COPY src/backend .
ENTRYPOINT ["gunicorn", "-c", "gunicorn.config.py"]
