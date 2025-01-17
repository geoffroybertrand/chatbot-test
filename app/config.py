from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # API Configuration
    CLAUDE_API_KEY: str
    CLAUDE_MODEL: str = "claude-3-opus-20240229"
    MAX_TOKENS: int = 1000

    # System Prompt
    SYSTEM_PROMPT: str = """Je suis un assistant spécialisé en thérapie systémique stratégique pratiquant une approche indirecte et contextualisée."""

    class Config:
        env_file = '.env'

settings = Settings()