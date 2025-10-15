from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./marketing.db"  # Default SQLite
    )
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    _API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()

if not settings.OPENAI_API_KEY:
    print("⚠️  OpenAI API key not configured")
if not settings.APIFY_API_TOKEN:
    print("⚠️  Apify API token not configured")
