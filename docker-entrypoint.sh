#!/bin/sh

poetry install --no-root

exec poetry run uvicorn run app:app --host 0.0.0.0 --port 8000 --reload
