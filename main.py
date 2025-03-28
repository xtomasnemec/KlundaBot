#!/usr/bin/env -S venv/bin/python3
import os

from dotenv import load_dotenv

from silverbot.start import run, SilverBotConfig

load_dotenv()


def env(key: str):
    val = os.environ.get(key)
    if val is None:
        raise EnvironmentError(f"Required environment variable {key} is not set")
    return val


run(SilverBotConfig(
    owner_id=int(env("owner_id")),
    management_guild=int(env("admin_guild_id")),
    management_channel=int(env("requests_channel")),
    open_weather_map_api_key=env("owm_api_key"),
    token=env("bot_token")
))
