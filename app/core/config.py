import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Raízes do Nordeste API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./raizes_nordeste.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sua_chave_secreta_jwt_super_segura")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()