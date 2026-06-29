from app.config.settings import get_settings
from app.llm.base import BaseLLMProvider
from app.llm.gemini_provider import GeminiProvider

def get_llm_provider() -> BaseLLMProvider: # Return type hint added for clarity
    settings = get_settings()

    if settings.LLM_PROVIDER.lower() == "gemini":
        return GeminiProvider()
    raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
