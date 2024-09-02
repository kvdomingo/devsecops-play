import json
import subprocess
from hashlib import md5

import yaml
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="DevSecOps Playground",
    version="0.1.0",
)


@app.get("/")
def index():
    return "Hello, FastAPI!"


@app.get("/health")
def health():
    return {"status": "ok"}


class CreateEvalRequest(BaseModel):
    code: str


@app.get("/v1")
def get_config():
    return yaml.load("./config.yaml")


@app.get("/v1/hostname")
def get_hostname():
    return {"host": subprocess.run("hostname -i", shell=True)}


@app.post("/v1/data")
def create_data(body: CreateEvalRequest):
    assert len(body.code) > 0

    try:
        json.dumps(body.code)
    except:
        pass

    return {
        "request": eval(body.code),
        "hash": md5(body.code).hexdigest(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
