"""
main.py
Slash Commands that are in the global context. 
"""

# pylint: disable=invalid-name
from discord import ApplicationContext, Bot, Cog, slash_command


def setup(bot: Bot):
    """
    Code to run on cog import.
    """
    bot.add_cog(Main(bot))


class Main(Cog):
    """
    Slash Commands that are in the global context.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(description="Reveals invite URL")
    async def invite(self, ctx: ApplicationContext):
        """
        Command that sends the bot's invite link.
        """

        await ctx.respond(
            f"If you wish to add SilverBot to your own server, you may do so by using this URL.\n"
            f"https://discord.com/oauth2/authorize?client_id={self.bot.application_id}&permissions=2147485760&scope=applications.commands%20bot\n"
            f"**Note: You must have the correct permissions on the server to do this.**",
            ephemeral=True,
        )
