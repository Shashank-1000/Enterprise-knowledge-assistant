from app.config.logging_config import setup_logging
from app.llm.provider_factory import get_llm_provider


setup_logging()

llm = get_llm_provider()

response = llm.generate(
    "In one sentence, say what a RAG system is."
)

print(response)