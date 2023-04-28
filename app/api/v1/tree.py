from typing import Optional
from fastapi import APIRouter, Request
from app.service import ProcessTree

from app.scheme import ParaphraseResponse

router = APIRouter()


@router.get("/paraphrase")
def paraphrase(
    request: Request, query: str, limit: Optional[int] = 20
) -> ParaphraseResponse:
    unique_btress = ProcessTree(query, limit).get_unique()
    return {"paraphrase": unique_btress}
