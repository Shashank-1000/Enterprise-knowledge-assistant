import logging

from app.config.logging_config import setup_logging
from app.retrieval.vector_index import VectorIndex


setup_logging()
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting vector index build")

    vector_index = VectorIndex()
    vector_index.build_from_chunks_file()

    print("FAISS vector index built successfully.")


if __name__ == "__main__":
    main()