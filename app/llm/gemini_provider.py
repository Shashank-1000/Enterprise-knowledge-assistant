import logging

from google import genai

from app.config.settings import get_settings
from app.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    """
    Gemini implementation of the LLM provider interface.
    """

    def __init__(self):
        settings = get_settings()

        self.model_name = settings.MODEL_NAME
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

        logger.info(f"GeminiProvider initialized with model: {self.model_name}")

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

            if not response or not response.text:
                return "I could not generate a response from the available context."

            return response.text.strip()

        except Exception as e:
            logger.exception("GeminiProvider encountered an error during generation.")
            raise RuntimeError(f"Error generating response: {str(e)}")

