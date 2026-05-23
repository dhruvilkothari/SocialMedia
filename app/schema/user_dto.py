from pydantic import BaseModel, field_validator, EmailStr, Field, ValidationError


class UserDto(BaseModel):
    name: str = Field(..., description="User's name", min_length=5, max_length=50)
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., description="'s password", min_length=5, max_length=50)
    profile_picture: str = Field(..., description="User's profile picture")
    is_active: bool = Field(description="User's active status", default=True)

    @field_validator("email")
    def validate_email(cls, v):
        allowed_domain = ["gmail", "yahoo", "outlook"]
        domain_value = v.split("@")[1]
        print("VALIDATION")
        print(domain_value)
        if domain_value.split(".")[0] not in allowed_domain:
            raise ValidationError("Invalid email address")
        return v




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


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., description="User's password")
