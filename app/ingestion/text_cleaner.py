import re


class TextCleaner:
    def clean(self, text: str) -> str:
        if not text:
            return ""

        text = text.replace("\u200b", "")
        text = text.replace("\xa0", " ")

        # Normalize repeated spaces/tabs
        text = re.sub(r"[ \t]+", " ", text)

        # Normalize repeated newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove excessive bullet artifacts but keep readable bullets
        text = text.replace("●​", "●")

        return text.strip()