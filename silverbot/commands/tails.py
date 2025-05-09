"""
tails.py
Slash Commands that represent Tails the Fox memes and other stuff.
"""

from discord import Embed, ApplicationContext, SlashCommandGroup, Bot, Cog


def setup(bot: Bot):
    """
    Code to run on cog import.
    """
    bot.add_cog(Tails(bot))


class Tails(Cog):
    """
    Slash Commands that represent Tails the Fox memes and other stuff.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    tails = SlashCommandGroup("tails", "Tails related fluff")

    @tails.command(description="make tails fluff his tail")
    async def tail(self, ctx: ApplicationContext):
        """
        Sends a gif in chat.
        """
        embed = Embed(
            title="Tails is now fluffing his tail.",
        )
        embed.set_image(
            url="https://media.discordapp.net/attachments/865374572789760030/1017083766881132574/modern_tails_sonic_generations_petting_namesakes_gif.gif"
        )
        await ctx.respond(embed=embed)

    @tails.command(description="Ask a local foxxo to ^W^ for you.")
    async def localfox(self, ctx: ApplicationContext):
        """
        Sends an image in chat.
        """
        embed = Embed(
            title="^W^",
        )
        embed.set_image(
            url="https://images-ext-2.discordapp.net/external/2SxYHvkOZPVMXM9gN6ieCC1T8W3fXF2NjUJndQLTaTo/https/i.imgur.com/250myup.jpg"
        )
        await ctx.respond(embed=embed)

    @tails.command(description="POG")
    async def pog(self, ctx: ApplicationContext):
        """
        Sends an image in chat.
        """
        embed = Embed(
            title="",
        )
        embed.set_image(url="https://i.imgur.com/RyWEDkY.png")
        await ctx.respond(embed=embed)
