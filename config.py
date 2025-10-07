from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://marketing_user:marketing_password_2024@localhost:5432/marketing_db")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

settings = Settings()

if not settings.OPENAI_API_KEY:
    print("⚠️  OpenAI API key not configured")
if not settings.APIFY_API_TOKEN:
    print("⚠️  Apify API token not configured")
