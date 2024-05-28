import subprocess
import os
from pathlib import Path


def get_output(command, *args, **kwargs):
    if kwargs.get("capture_output") is None:
        kwargs["capture_output"] = True
    return subprocess.run(command, *args, **kwargs).stdout.decode("utf-8").strip()


def update():
    assert subprocess.run("git pull origin main").returncode == 0


def create_data_clone():
    assert (
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
            shell=True,
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            [
                "git",
                "config",
                "user.name",
                "SilverBot",
            ],
            cwd=ASSET_DIRECTORY,
            shell=True,
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            [
                "git",
                "config",
                "user.email",
                "",
            ],
            cwd=ASSET_DIRECTORY,
            shell=True,
        ).returncode
        == 0
    )


def add_asset(file, path: str):
    path = ASSET_DIRECTORY / path
    path.parent.mkdir(parents=True, exist_ok=True)
    f = open(path, mode="wb")
    f.write(file)
    f.close()
    assert (
        subprocess.run(
            ["git", "add", str(path)], cwd=ASSET_DIRECTORY, shell=True
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            ["git", "commit", "-m", "auto: Upload asset"],
            cwd=ASSET_DIRECTORY,
            shell=True,
        ).returncode
        == 0
    )
    assert (
        subprocess.run(
            [f"git", "push", "origin", "assets"], cwd=ASSET_DIRECTORY, shell=True
        ).returncode
        == 0
    )


ASSET_DIRECTORY_NAME = "silverbot_data"
REMOTE_URL = get_output("git remote get-url origin")
BOT_DIRECTORY = Path(get_output("git rev-parse --show-toplevel"))
ASSET_DIRECTORY = BOT_DIRECTORY / ASSET_DIRECTORY_NAME
if not ASSET_DIRECTORY.exists():
    print("Asset directory not found, cloning and setting it up for you.")
    create_data_clone()
