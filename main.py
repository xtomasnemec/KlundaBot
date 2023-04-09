import asyncio
import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv

from utils.error_message import panic
from assets.status_messages import status_messages

load_dotenv()

# Environment variables
bot_token = os.environ.get("bot_token")
owner_id = int(os.environ.get("owner_id", "0"))

# The user account
bot = discord.Bot(owner_id=owner_id)

# Extensions to load initially
COGS = [x[:-3] for x in os.listdir("commands") if x.endswith(".py")]
for cog in COGS:
    bot.load_extension(f"commands.{cog}")


# Cycle through status messages
@tasks.loop(seconds=20)
async def status():
    msg = status_messages[status.current_loop % 4]
    msg = msg.format(servers=len(bot.guilds))
    await bot.change_presence(activity=discord.Game(msg))


# Send message on unhandled error
@bot.event
async def on_application_command_error(
    ctx: discord.ApplicationContext, error: discord.DiscordException
):
    await asyncio.sleep(0.15)
    if not (isinstance(ctx.options, dict) and ctx.options.get("handled") == True):
        await panic(ctx, f"{error}")


# Report when logged in
@bot.event
async def on_ready():
    print("✅ Bot logged in")
    print(f"ID: {bot.user.id}, Username: {bot.user.name}")
    status.start()


bot.run(bot_token)
