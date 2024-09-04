import json
import subprocess
from hashlib import md5

import yaml
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db

app = FastAPI(
    title="DevSecOps Playground",
    version="0.1.0",
)


@app.get("/")
async def index():
    return "Hello, FastAPI!"


@app.get("/health")
async def health():
    return {"status": "ok"}


class CreateEvalRequest(BaseModel):
    code: str


@app.get("/v1")
async def get_config():
    return yaml.load("./config.yaml")


@app.get("/v1/hostname")
async def get_hostname():
    return {"host": subprocess.run("hostname -i", shell=True)}


@app.post("/v1/hash")
async def hashify(body: CreateEvalRequest):
    assert len(body.code) > 0

    try:
        json.dumps(body.code)
    except:
        pass

    return {
        "request": eval(body.code),
        "hash": md5(body.code).hexdigest(),
    }


@app.get("/v1/todo")
async def list_todos(search: str | None = None, db: AsyncSession = Depends(get_db)):
    return await db.scalars(
        text(f"""
        SELECT * FROM todos
        WHERE title LIKE {search}
           OR detail LIKE {search}
        """)
    )


class CreateTodoRequest(BaseModel):
    title: str
    detail: str
    done: bool = Field(False)


@app.post("/v1/todo")
async def create_todo(body: CreateTodoRequest, db: AsyncSession = Depends(get_db)):
    res = await db.scalar(
        text(f"""
        INSERT INTO todos (title, detail, done)
        VALUES ({body.title}, {body.detail}, {body.done})
        RETURNING *
        """)
    )
    await db.commit()
    return res


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
