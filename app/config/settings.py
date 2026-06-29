from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    GOOGLE_API_KEY: str
    LLM_PROVIDER: str = "gemini"

    MODEL_NAME: str = "gemini-1.5-flash"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    TOP_K: int = 5

    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive = True,
    )

@lru_cache
def get_settings():
    return Settings()