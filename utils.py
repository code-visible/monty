import hashlib


def caculate_hash_id(info: str) -> str:
    return hashlib.md5(info.encode()).hexdigest()


# TODO: better recognize and parse other files ?
def is_source(file_path: str) -> bool:
    return file_path.endswith(".py")


def format_path(path: str) -> str:
    if path == ".":
        return "/"
    if not path.startswith("/"):
        return "/%s" % path
