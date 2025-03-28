from dataclasses import dataclass
import discord
from discord.ext import tasks
import silverbot.commands

from utils.embeds import error_critical

_STATUS_MESSAGES = [
    "in {servers} servers",
    "with psychokinetic power",
    "𝙄𝙏'𝙎 𝙉𝙊 𝙐𝙎𝙀!",
    "🦔 goes brrr",
]


@dataclass
class SilverBotConfig:
    owner_id: int
    token: str
    open_weather_map_api_key: str
    management_guild: int
    management_channel: int


def run(config: SilverBotConfig):
    # The user account
    bot = discord.Bot(owner_id=config.owner_id)

    # Extensions to load initially
    for cog in silverbot.commands.list():
        bot.load_extension(f"commands.{cog}")

    # Cycle through status messages
    @tasks.loop(seconds=20)
    async def status():
        msg = _STATUS_MESSAGES[status.current_loop % 4]
        msg = msg.format(servers=len(bot.guilds))
        await bot.change_presence(activity=discord.Game(msg))

    # Send message on unhandled error
    @bot.event
    async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
        await ctx.respond(embed=error_critical(str(error)), ephemeral=True)

    # Report when logged in
    @bot.event
    async def on_ready():
        print("✅ Bot logged in")
        print(f"ID: {bot.user.id}, Username: {bot.user.name}")
        status.start()

    bot.run(config.token)
