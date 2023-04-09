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

    @slash_command(description="give out pets to various furballs")
    async def pet(
        self,
        ctx: discord.ApplicationContext,
        who: Option(
            str,
            "Who do you want to pet?",
            choices=[
                OptionChoice(name=character, value=str(index))
                for index, character in enumerate(assets.pet.characters)
            ],
        ),
    ):
        """
        Command that sends a specified petting gif.
        """
        pet_who: str = assets.pet.characters[int(who)]
        embed = discord.Embed(
            title=f"{ctx.author.name} is petting {pet_who}!",
        )
        embed.set_image(
            url=f"https://raw.githubusercontent.com/Silver-Volt4/SilverBot/master/assets/pet/{pet_who.lower()}.gif"
        )
        await ctx.respond(embed=embed)
