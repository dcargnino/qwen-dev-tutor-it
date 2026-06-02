def normalize_username(username: str) -> str:
    cleaned = username.strip().lower()
    return cleaned.replace(" ", "_")

