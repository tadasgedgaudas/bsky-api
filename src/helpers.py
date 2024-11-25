def get_record_key(url: str) -> str:
    return url.split("/")[-1]
