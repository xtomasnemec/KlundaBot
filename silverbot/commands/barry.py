"""
silv.py
Slash Commands that represent Silver the Hedgehog memes and other stuff.
"""

from discord import Bot, Cog, SlashCommandGroup, ApplicationContext, User, Embed

from silverbot.utils import embeds


def setup(bot: Bot):
    """
    Code to run on cog import.
    """
    cog = Barry(bot)
    bot.add_cog(cog)

    # Manually trigger decorators.
    bot.user_command(name="🔴 Send Barry hug")(cog.hug)


class Barry(Cog):
    """
    Slash Commands that represent Silver the Hedgehog memes and other stuff.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    barry = SlashCommandGroup("barry", "Barry the Quokka fluff")

    @barry.command(name="hug", description="Gift somebody a warm hug!")
    async def _hug(self, ctx: ApplicationContext, user: User):
        await self.hug(ctx, user)

    async def hug(self, ctx: ApplicationContext, user: User):
        """
        Sends a hug to a specified user.
        """
        hug_from = ctx.author.mention
        if user == ctx.author:
            hug_from = self.bot.user.mention
        embed = embeds.base(
            Embed(
                title="Aww, I love hugs! 😊",
                description=f"{hug_from} *hugs* {user.mention}",
            ),
            footer_additional="Art by @shadows-coffeebeans",
        )
        embed.set_image(
            url="https://raw.githubusercontent.com/Silver-Volt4/SilverBot/assets/barry_hug.png"
        )
        await ctx.respond(embed=embed)
