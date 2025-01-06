import hashlib


def caculate_hash_id(info: str) -> str:
    return hashlib.md5(info.encode()).hexdigest()
