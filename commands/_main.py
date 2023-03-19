import importlib
import discord
from discord import slash_command
from discord.commands import OptionChoice
from discord.ext import commands
import data.pet


def setup(bot: discord.Bot):
    importlib.reload(data.pet)
    bot.add_cog(Main(bot))


class Main(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="give out pets to various furballs")
    async def pet(
        self,
        ctx: discord.ApplicationContext,
        who: discord.Option(
            str,
            "Who do you want to pet?",
            choices=[
                OptionChoice(name=p[0], value=str(i))
                for i, p in enumerate(data.pet.pet)
            ],
        ),
    ):
        pet_who = data.pet.pet[int(who)]
        embed = discord.Embed(
            title=f"{ctx.author.name} is petting {pet_who[0]}!",
        )
        embed.set_image(url=pet_who[1])
        await ctx.respond(embed=embed)
