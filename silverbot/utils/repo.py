import subprocess
from pathlib import Path


def get_output(command, *args, **kwargs):
    if kwargs.get("capture_output") is None:
        kwargs["capture_output"] = True
    return subprocess.run(command, *args, **kwargs).stdout.decode("utf-8").strip()


def update():
    subprocess.run(["git", "pull", "origin", "main"]).check_returncode()


def create_data_clone():
    subprocess.run(
        [
            "git",
            "clone",
            "-b",
            "assets",
            "--single-branch",
            REMOTE_URL,
            ASSET_DIRECTORY_NAME,
        ],
        cwd=BOT_DIRECTORY,
    ).check_returncode()

    subprocess.run(
        [
            "git",
            "config",
            "user.name",
            "SilverBot",
        ],
        cwd=ASSET_DIRECTORY,
    ).check_returncode()

    subprocess.run(
        [
            "git",
            "config",
            "user.email",
            "",
        ],
        cwd=ASSET_DIRECTORY,
    ).check_returncode()


def add_asset(file, path: str):
    path = ASSET_DIRECTORY / path
    path.parent.mkdir(parents=True, exist_ok=True)
    f = open(path, mode="wb")
    f.write(file)
    f.close()
    subprocess.run(["git", "add", str(path)], cwd=ASSET_DIRECTORY).check_returncode()
    subprocess.run(
        ["git", "commit", "-m", "auto: Upload asset"], cwd=ASSET_DIRECTORY
    ).check_returncode()
    subprocess.run(
        ["git", "push", "origin", "assets"], cwd=ASSET_DIRECTORY
    ).check_returncode()


ASSET_DIRECTORY_NAME = "silverbot_data"
REMOTE_URL = get_output(["git", "remote", "get-url", "origin"])
BOT_DIRECTORY = Path(get_output(["git", "rev-parse", "--show-toplevel"]))
ASSET_DIRECTORY = BOT_DIRECTORY / ASSET_DIRECTORY_NAME
if not ASSET_DIRECTORY.exists():
    print("Asset directory not found, cloning and setting it up for you.")
    create_data_clone()
