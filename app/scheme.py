from typing import Optional
import pydantic


class CBTree(pydantic.BaseModel):
    text: str


class ParaphraseResponse(pydantic.BaseModel):
    paraphrase: list[CBTree]
