import hashlib
import logging
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import get_settings
from app.ingestion.metadata_extractor import MetadataExtractor
from app.ingestion.text_cleaner import TextCleaner
from app.ingestion.validators import ChunkValidator
from app.models.document_models import DocumentPage, DocumentChunk

logger = logging.getLogger(__name__)


class DocumentChunker:
    def __init__(self):
        settings = get_settings()

        self.cleaner = TextCleaner()
        self.metadata_extractor = MetadataExtractor()
        self.validator = ChunkValidator()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""],
        )

    def _generate_chunk_id(
        self,
        document_name: str,
        page_number: int,
        chunk_index: int,
        text: str,
    ) -> str:
        raw_id = f"{document_name}-{page_number}-{chunk_index}-{text[:80]}"
        return hashlib.md5(raw_id.encode("utf-8")).hexdigest()

    def chunk_pages(self, pages: List[DocumentPage]) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []

        for page in pages:
            cleaned_text = self.cleaner.clean(page.text)

            if not cleaned_text:
                continue

            section_title = self.metadata_extractor.extract_section_title(cleaned_text)

            split_texts = self.splitter.split_text(cleaned_text)

            for idx, text in enumerate(split_texts):
                cleaned_chunk = self.cleaner.clean(text)

                if not self.validator.is_valid(cleaned_chunk):
                    continue

                chunk_id = self._generate_chunk_id(
                    page.document_name,
                    page.page_number,
                    idx,
                    cleaned_chunk,
                )

                chunk = DocumentChunk(
                    chunk_id=chunk_id,
                    document_name=page.document_name,
                    document_path=page.document_path,
                    page_number=page.page_number,
                    chunk_index=idx,
                    text=cleaned_chunk,
                    section_title=section_title,
                    metadata={
                        "document_name": page.document_name,
                        "document_path": page.document_path,
                        "page_number": page.page_number,
                        "chunk_index": idx,
                        "section_title": section_title,
                    },
                )

                chunks.append(chunk)

        logger.info(f"Created {len(chunks)} valid chunks from {len(pages)} pages")
        return chunks