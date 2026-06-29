import logging
from pathlib import Path
from typing import List

import fitz  # PyMuPDF
from docx import Document as DocxDocument
from bs4 import BeautifulSoup

from app.models.document_models import DocumentPage

logger = logging.getLogger(__name__)


class DocumentLoader:
    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx", ".html", ".htm"}

    def load_file(self, file_path: str) -> List[DocumentPage]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = path.suffix.lower()

        if suffix not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {suffix}")

        if suffix == ".pdf":
            return self.load_pdf(path)

        if suffix in {".txt", ".md"}:
            return self.load_text_file(path)

        if suffix == ".docx":
            return self.load_docx(path)

        if suffix in {".html", ".htm"}:
            return self.load_html(path)

        raise ValueError(f"Unsupported file type: {suffix}")

    def load_pdf(self, path: Path) -> List[DocumentPage]:
        logger.info(f"Loading PDF: {path.name}")

        pages: List[DocumentPage] = []

        with fitz.open(str(path)) as doc:
            for page_index, page in enumerate(doc):
                text = page.get_text("text").strip()

                if not text:
                    continue

                pages.append(
                    DocumentPage(
                        document_name=path.name,
                        document_path=str(path),
                        page_number=page_index + 1,
                        text=text,
                    )
                )

        logger.info(f"Loaded {len(pages)} pages from {path.name}")
        return pages

    def load_text_file(self, path: Path) -> List[DocumentPage]:
        logger.info(f"Loading text/markdown file: {path.name}")

        text = path.read_text(encoding="utf-8", errors="ignore").strip()

        if not text:
            return []

        return [
            DocumentPage(
                document_name=path.name,
                document_path=str(path),
                page_number=1,
                text=text,
            )
        ]

    def load_docx(self, path: Path) -> List[DocumentPage]:
        logger.info(f"Loading DOCX: {path.name}")

        doc = DocxDocument(str(path))
        paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
        text = "\n".join(paragraphs)

        if not text:
            return []

        return [
            DocumentPage(
                document_name=path.name,
                document_path=str(path),
                page_number=1,
                text=text,
            )
        ]

    def load_html(self, path: Path) -> List[DocumentPage]:
        logger.info(f"Loading HTML: {path.name}")

        html = path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n").strip()

        if not text:
            return []

        return [
            DocumentPage(
                document_name=path.name,
                document_path=str(path),
                page_number=1,
                text=text,
            )
        ]

    def load_directory(self, directory_path: str) -> List[DocumentPage]:
        directory = Path(directory_path)

        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        all_pages: List[DocumentPage] = []

        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                pages = self.load_file(str(file_path))
                all_pages.extend(pages)

        logger.info(f"Loaded total {len(all_pages)} document pages from {directory_path}")
        return all_pages