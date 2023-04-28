from typing import Optional
from fastapi import APIRouter, Request, HTTPException
from app.service import ProcessTree

from app.scheme import ParaphraseResponse, ParaphraseRequest

router = APIRouter()


@router.get("/paraphrase")
def paraphrase(
    request: Request, query: str, limit: Optional[int] = 20
) -> ParaphraseResponse:
    # Non-negative limit
    try:
        ParaphraseRequest(query=query, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=exc.errors())

    limit = limit if limit > 0 else 20
    unique_btress = ProcessTree(query, limit).get_unique()
    return {"paraphrase": unique_btress}
