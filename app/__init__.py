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


@app.post("/v1")
def create_eval(body: CreateEvalRequest):
    return {"data": eval(body.code)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
