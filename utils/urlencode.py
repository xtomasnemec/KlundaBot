from urllib.parse import quote


def urlencode(string):
    return quote(string.encode("utf-8"))
