class ChunkValidator:
    def is_valid(self, text: str) -> bool:
        if not text:
            return False

        text = text.strip()

        if len(text) < 40:
            return False

        alpha_chars = sum(char.isalpha() for char in text)
        alpha_ratio = alpha_chars / max(len(text), 1)

        if alpha_ratio < 0.35:
            return False

        return True