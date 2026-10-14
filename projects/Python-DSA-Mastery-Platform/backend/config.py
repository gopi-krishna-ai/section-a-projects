import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Python & DSA Mastery Platform"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./python_dsa_mastery.db")
    SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY", "python_dsa_mastery_secret_auth_2026")
    TOKEN_EXPIRY_DAYS: int = 14

    # Secure code execution limits
    EXEC_TIMEOUT_SECONDS: float = float(os.getenv("EXEC_TIMEOUT_SECONDS", "4.0"))
    EXEC_MAX_OUTPUT_BYTES: int = 100 * 1024 # 100 KB max stdout/stderr

    # AI Configuration (Optional with rich deterministic fallback)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")

    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()
