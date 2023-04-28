from fastapi import FastAPI

app = FastAPI()

from app.api.v1 import tree

app.include_router(tree.router)


@app.get("/")
def hello():
    return {"msg": "hello"}
