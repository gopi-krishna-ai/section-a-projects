"""
config.py — Application configuration for different environments.

Usage in app.py:
    from config import config
    app.config.from_object(config["development"])
"""

import os
from datetime import timedelta


class BaseConfig:
    """Shared configuration for all environments."""
    SECRET_KEY         = os.environ.get("SECRET_KEY", "study-planner-secret-dev-2026")
    JWT_SECRET_KEY     = os.environ.get("JWT_SECRET", "jwt-secret-dev-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS     = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit


class DevelopmentConfig(BaseConfig):
    """Development environment — SQLite, Debug ON."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "sqlite:///study_planner_dev.db"
    )
    SQLALCHEMY_ECHO = False  # Set True to log SQL queries


class TestingConfig(BaseConfig):
    """Testing environment — in-memory SQLite."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production environment — PostgreSQL, Debug OFF."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://user:password@localhost/study_planner_prod"
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    SESSION_COOKIE_SECURE    = True
    SESSION_COOKIE_HTTPONLY  = True
    SESSION_COOKIE_SAMESITE  = "Lax"


config = {
    "development": DevelopmentConfig,
    "testing":     TestingConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}
