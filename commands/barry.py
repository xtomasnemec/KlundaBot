"""
silv.py
Slash Commands that represent Silver the Hedgehog memes and other stuff.
"""

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup


def setup(bot: discord.Bot):
    """
    Code to run on cog import.
    """
    cog = Barry(bot)
    bot.add_cog(cog)

    # Manually trigger decorators.
    bot.user_command(name="🔴 Send Barry hug")(cog.hug)


class Barry(commands.Cog):
    """
    Slash Commands that represent Silver the Hedgehog memes and other stuff.
    """

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    barry = SlashCommandGroup("barry", "Barry the Quokka fluff")

    @barry.command(name="hug", description="Gift somebody a warm hug!")
    async def _hug(self, ctx: discord.ApplicationContext, user: discord.User):
        await self.hug(ctx, user)

    async def hug(self, ctx: discord.ApplicationContext, user: discord.User):
        """
        Sends a hug to a specified user.
        """
        hug_from = ctx.author.mention
        if user == ctx.author:
            hug_from = self.bot.user.mention
        embed = discord.Embed(title="Aww, I love hugs! 😊", description=f"{hug_from} *hugs* {user.mention}")
        embed.set_image(url="https://raw.githubusercontent.com/Silver-Volt4/SilverBot/assets/barry_hug.png")
        embed.set_footer(text="SilvBot | Art by @shadows-coffeebeans")
        await ctx.respond(embed=embed)
