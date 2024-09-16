def truncate(text: str, size: int) -> str:
    if len(text) < size:
        return text
    else:
        return text[:size-3] + '...'
