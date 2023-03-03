import asyncio
import discord
import os
from util.error_message import panic

bot_token = os.environ.get("bot_token")

COGS = [x[:-3] for x in os.listdir("commands") if x.endswith(".py")]

bot = discord.Bot(
    owner_id=276742341031755776
)


for cog in COGS:
    bot.load_extension(
        f"commands.{cog}",
    )


@bot.event
async def on_ready():
    while True:
        for msg in [
            "in {0} servers".format(len(bot.guilds)),
            "with psychokinetic power",
            "IT'S NO USE!", "Just being fluffy af"
        ]:
            await bot.change_presence(activity=discord.Game(msg))
            await asyncio.sleep(20)


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    await asyncio.sleep(0.15)
    if isinstance(ctx.options,dict) and ctx.options.get("handled") == True:
        pass
    else:
        await panic(ctx, f"{error}")

bot.run(bot_token)
