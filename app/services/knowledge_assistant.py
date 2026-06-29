import logging
from typing import Dict, Any, List

from app.llm.provider_factory import get_llm_provider
from app.prompts.rag_prompt import build_rag_prompt
from app.retrieval.retriever import RetrieverService
from app.schemas.chat import ChatResponse, SourceReference
import time

logger = logging.getLogger(__name__)


class KnowledgeAssistantService:
    """
    Orchestrates the full RAG flow:
    question -> retrieval -> prompt construction -> LLM answer -> source citations.
    """

    def __init__(self):
        self.retriever = RetrieverService()
        self.llm = get_llm_provider()

    def answer_question(self, question: str) -> ChatResponse:
        start_time = time.perf_counter()
        retrieved_chunks = self.retriever.retrieve(question)

        if not retrieved_chunks:
            return ChatResponse(
                answer="I could not find relevant information in the provided documents.",
                sources=[],
                confidence=0.0,
                retrieved_chunks=0,
            )

        top_chunks = retrieved_chunks[:5]

        prompt = build_rag_prompt(
            question=question,
            retrieved_chunks=top_chunks,
        )

        answer = self.llm.generate(prompt)

        sources = self._build_sources(top_chunks)
        confidence = self._estimate_confidence(top_chunks)
        processing_time_ms = round(
            (time.perf_counter() - start_time)*1000, 2, # Convert to milliseconds and round to 2 decimal places
        )

        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            retrieved_chunks=len(retrieved_chunks),
            processing_time_ms=processing_time_ms,
        )

    def _build_sources(
        self,
        retrieved_chunks: List[Dict[str, Any]],
    ) -> List[SourceReference]:
        sources = []
        seen = set()

        for chunk in retrieved_chunks:
            metadata = chunk["metadata"]

            source_key = (
                metadata.get("document_name"),
                metadata.get("page_number"),
                metadata.get("section_title"),
            )

            if source_key in seen:
                continue

            seen.add(source_key)

            sources.append(
                SourceReference(
                    document=metadata.get("document_name"),
                    page=metadata.get("page_number"),
                    section=metadata.get("section_title"),
                )
            )

        return sources

    def _estimate_confidence(
        self,
        retrieved_chunks: List[Dict[str, Any]],
    ) -> float:
        if not retrieved_chunks:
            return 0.0

        best_distance = retrieved_chunks[0].get("distance", 1.0)
        confidence = 1.0 / (1.0 + best_distance)

        return round(confidence, 2)