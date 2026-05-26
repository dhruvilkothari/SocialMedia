from pydantic import BaseModel, Field


class CommentDto(BaseModel):
    body: str = Field(..., min_length=1, max_length=500)