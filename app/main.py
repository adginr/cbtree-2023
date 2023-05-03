from fastapi import FastAPI

app = FastAPI()

from app.api.v1 import tree

app.include_router(tree.router)


@app.get("/")
def main() -> dict[str, str]:
    return {"msg": "Hello World"}
