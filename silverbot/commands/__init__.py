import os


def list() -> list[str]:
    return [
        filename[:-3]  # remove .py suffix
        for filename in os.listdir(__path__[0])
        if filename != "__init__.py" and filename.endswith(".py")
    ]
