from typing import Optional
import pydantic
from nltk.tree.tree import Tree


class CBTree(pydantic.BaseModel):
    text: str


class ParaphraseResponse(pydantic.BaseModel):
    paraphrase: list[CBTree]


class ParaphraseRequest(pydantic.BaseModel):
    query: str
    limit: int

    @pydantic.validator("query")
    def validate_query(cls, v):
        Tree.fromstring(v)
        return v
