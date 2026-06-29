import json
import logging
from pathlib import Path

from app.config.logging_config import setup_logging
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.chunker import DocumentChunker


setup_logging()
logger = logging.getLogger(__name__)


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DATA_DIR / "chunks.json"


def main():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    loader = DocumentLoader()
    chunker = DocumentChunker()

    pages = loader.load_directory(str(RAW_DATA_DIR))
    chunks = chunker.chunk_pages(pages)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [chunk.model_dump() for chunk in chunks],
            f,
            indent=2,
            ensure_ascii=False,
        )

    logger.info(f"Saved chunks to {OUTPUT_FILE}")
    print(f"Successfully processed {len(chunks)} chunks.")


if __name__ == "__main__":
    main()