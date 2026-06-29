import json
import logging
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.config.settings import get_settings
from app.models.document_models import DocumentChunk

logger = logging.getLogger(__name__)


class VectorIndex:
    def __init__(self):
        settings = get_settings()

        self.index_path = Path("data/vector_store/faiss_index")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            encode_kwargs={"normalize_embeddings": True},
        )

    def _convert_chunks_to_documents(
        self,
        chunks: List[DocumentChunk],
    ) -> List[Document]:
        documents = []

        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk.text,
                    metadata={
                        "chunk_id": chunk.chunk_id,
                        "document_name": chunk.document_name,
                        "document_path": chunk.document_path,
                        "page_number": chunk.page_number,
                        "chunk_index": chunk.chunk_index,
                        "section_title": chunk.section_title,
                    },
                )
            )

        return documents

    def build_from_chunks_file(
        self,
        chunks_file: str = "data/processed/chunks.json",
    ) -> FAISS:
        chunks_path = Path(chunks_file)

        if not chunks_path.exists():
            raise FileNotFoundError(
                f"{chunks_file} not found. Run ingestion first."
            )

        with open(chunks_path, "r", encoding="utf-8") as f:
            raw_chunks = json.load(f)

        chunks = [DocumentChunk(**chunk) for chunk in raw_chunks]
        documents = self._convert_chunks_to_documents(chunks)

        if not documents:
            raise ValueError("No documents available for indexing.")

        logger.info(f"Building FAISS index from {len(documents)} chunks")

        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_model,
        )

        self.index_path.mkdir(parents=True, exist_ok=True)
        vector_store.save_local(str(self.index_path))

        logger.info(f"Saved FAISS index to {self.index_path}")

        return vector_store

    def load(self) -> FAISS:
        if not self.index_path.exists():
            raise FileNotFoundError(
                "FAISS index not found. Run build_index first."
            )

        vector_store = FAISS.load_local(
            folder_path=str(self.index_path),
            embeddings=self.embedding_model,
            allow_dangerous_deserialization=True,
        )

        logger.info("Loaded FAISS index successfully")
        return vector_store