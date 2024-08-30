FROM python:3.11-alpine3.19

WORKDIR /tmp

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create false

WORKDIR /app

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
