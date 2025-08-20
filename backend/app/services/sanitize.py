import re

def sanitize(text: str, max_len: int | None = None) -> str:
    if not text:
        return text
    # remove known junk
    text = re.sub(r"^You ONLY have access.*$", "", text)  # Crew tool spec leakage
    text = re.sub(r"^IMPORTANT: Use the following format.*$", "", text)  # Prevents any extra tool output
    # collapse whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if max_len and len(text) > max_len:
        text = text[:max_len].rstrip() + "..."
    return text
