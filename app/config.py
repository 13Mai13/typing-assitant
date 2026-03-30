"""Application configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # App settings
    app_name: str = "Typing Assistant"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./typing_assistant.db"

    # Lesson progression
    default_confidence_threshold: float = 1.0
    default_wpm_threshold: float = 35.0
    default_accuracy_threshold: float = 0.95

    # Session settings
    min_session_duration: int = 10  # seconds

    # Code practice
    code_problems_dir: str = "app/data/code_problems"


settings = Settings()
