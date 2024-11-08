
def sanitize_filename(text: str) -> str:
    return text.strip().replace('/', '_').replace('\\', '_')
