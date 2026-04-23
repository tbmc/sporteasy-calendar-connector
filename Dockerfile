FROM node:24-slim AS build-web-app

WORKDIR /app

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

RUN wget -qO- https://get.pnpm.io/install.sh | sh -
COPY . .
RUN cd web-app && npm install --global corepack@latest && env pnpm install && pnpm build

RUN mv ./web-app/build ./temp-build \
    && rm -rf ./web-app \
    && mkdir -p ./web-app/ \
    && mv ./temp-build ./web-app/build


FROM python:3.14.4-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY . .
RUN rm -rf web-app
COPY --from=build-web-app /app/web-app/build /app/web-app/build
RUN uv sync

CMD ["uv", "run", "gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "--access-logfile", "/logs/access.log", "--error-logfile", "/logs/error.log", "app:app"]
