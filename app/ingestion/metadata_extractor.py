import re
from typing import Optional


class MetadataExtractor:
    def extract_section_title(self, text: str) -> Optional[str]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if not lines:
            return None

        for line in lines[:5]:
            if self._looks_like_heading(line):
                return line

        return None

    def _looks_like_heading(self, line: str) -> bool:
        if len(line) > 80:
            return False

        if line.endswith("."):
            return False

        heading_patterns = [
            r"^\d+\.?\s+[A-Z].*",
            r"^[A-Z][A-Za-z\s\-&/]{3,}$",
            r"^[A-Z][A-Za-z\s]+:$",
        ]

        return any(re.match(pattern, line) for pattern in heading_patterns)