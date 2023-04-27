from typing import Optional
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/paraphrase")
def paraphrase(request: Request, query: str, limit: Optional[int] = 20):
    return {"msg": "hello", "query": query, "limit": limit}
