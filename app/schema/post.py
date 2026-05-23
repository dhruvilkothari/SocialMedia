from fastapi import UploadFile
from pydantic import BaseModel, Field


from pydantic import BaseModel, Field

class PostDto(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    body: str = Field(..., min_length=5, max_length=100)

    class Config:
        from_attributes = True