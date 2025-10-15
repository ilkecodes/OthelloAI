import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://marketing_user:marketing_password_2024@localhost:5432/marketing_db")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    APIFY_API_TOKEN: str = os.getenv("APIFY_API_TOKEN", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    class Config:
        env_file = ".env"

settings = Settings()

# Warning messages (optional attributes)
if not settings.OPENAI_API_KEY:
    print("⚠️  OpenAI API key not configured")

if not settings.APIFY_API_TOKEN:
    print("⚠️  Apify API token not configured")
