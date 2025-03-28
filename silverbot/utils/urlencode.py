from urllib.parse import quote


def urlencode(string: str):
    return quote(string.encode("utf-8"))
