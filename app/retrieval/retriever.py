import logging
from typing import List, Dict, Any

from app.config.settings import get_settings
from app.retrieval.vector_index import VectorIndex


logger = logging.getLogger(__name__)


class RetrieverService:
    """
    Responsible for retrieving the most relevant document chunks
    from the FAISS vector store.
    """

    def __init__(self):
        settings = get_settings()

        self.top_k = settings.TOP_K

        vector_index = VectorIndex()
        self.vector_store = vector_index.load()

        logger.info("Retriever initialized successfully.")

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks along with similarity scores.
        """

        logger.info(f"Searching for query: {query}")

        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=self.top_k,
        )

        retrieved_chunks = []

        for document, score in results:
            retrieved_chunks.append(
                {
                    "content": document.page_content,
                    "metadata": document.metadata,
                    "distance": float(score),
                }
            )

        logger.info(f"Retrieved {len(retrieved_chunks)} chunks")

        return retrieved_chunks