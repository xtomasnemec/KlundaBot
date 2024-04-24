"""
main.py
Slash Commands that are in the global context. 
"""

# pylint: disable=invalid-name
import importlib
import discord
from discord.commands import OptionChoice, slash_command, Option
from discord.ext import commands

import assets.pet


def setup(bot: discord.Bot):
    """
    Code to run on cog import.
    """
    importlib.reload(assets.pet)
    bot.add_cog(Main(bot))


class Main(commands.Cog):
    """
    Slash Commands that are in the global context.
    """

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Reveals invite URL")
    async def invite(self, ctx: discord.ApplicationContext):
        """
        Command that sends the bot's invite link.
        """

        await ctx.respond(
            "If you wish to add SilverBot to your own server, you may do so by using this URL.\n"
            + "https://discord.com/oauth2/authorize?client_id=1014210710559006803&permissions=2147485760&scope=applications.commands%20bot\n"
            + "**Note: You must have the correct permissions on the server to do this.**",
            ephemeral=True,
        )
