import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Aptitude Mastery Coach"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./aptitude_coach.db")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini") # gemini, openai, or local_rule
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()
