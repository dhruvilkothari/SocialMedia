from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    description: str
    title: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiry: int
    db_url: str

    class Config:
        env_file = ".env"


settings = Settings()