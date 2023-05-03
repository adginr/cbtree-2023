from fastapi import APIRouter, Request, HTTPException
from app.service import ProcessTree
from pydantic import ValidationError
from app.scheme import ParaphraseResponse, ParaphraseRequest

router = APIRouter()

LIMIT = 20


@router.get("/paraphrase", response_model=ParaphraseResponse)
def paraphrase(
    request: Request, query: str, limit: int = LIMIT
) -> dict[str, list[dict[str, str]]]:
    try:
        ParaphraseRequest(query=query, limit=limit)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors())

    unique_btress = ProcessTree(query, limit).get_unique()

    return {"paraphrase": unique_btress}
