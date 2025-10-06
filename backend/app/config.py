from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    APIFY_API_TOKEN: str
    SECRET_KEY: str = "temp-secret-key"
    ALGORITHM: str = "HS256"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    openai_api_key: str = "" 
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
