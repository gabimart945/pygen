def sanitize_filename(text: str) -> str:
    """
    Sanitizes a filename by removing leading and trailing whitespace and replacing
    potentially problematic characters with underscores.

    This function ensures that the provided text can safely be used as a filename by
    replacing forward slashes (`/`) and backslashes (`\\`) with underscores (`_`).

    Args:
        text (str): The input text to sanitize.

    Returns:
        str: A sanitized version of the input text with problematic characters replaced.

    Example:
        >>> sanitize_filename(" /my\\file\\name ")
        '_my_file_name'
    """
    return text.strip().replace('/', '_').replace('\\', '_')
