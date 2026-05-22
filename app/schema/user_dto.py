from pydantic import BaseModel, field_validator, EmailStr, Field
class UserDto(BaseModel):
    name: str = Field(..., description="User's name", min_length=5, max_length=50)
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., description="'s password", min_length=5, max_length=50)
    profile_picture: str = Field(..., description="User's profile picture")
    is_active: bool = Field(description="User's active status", default=True)

    class Config:
        schema_extra = {
            "example": {
                "name": "dhruvil",
                "email": "kotharidhruvil3@gmail.com",
                "password": "123456789",
                "profile_picture": "/static/img/dhruvil.png"
            }
        }
        from_attributes = True

