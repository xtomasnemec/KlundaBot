"""
manage.py
Slash Commands that are meant to be used by whoever is hosting the bot.
"""
import asyncio
import os

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from utils.error_message import apologize


character = [
    # Hoisted characters
    ["silver", "Silver"],
    ["barry", "Barry"],
    # The rest is ordered alphabetically
    ["amy", "Amy"],
    ["bean", "Bean"],
    ["blaze", "Blaze"],
    ["cream", "Cream"],
    ["eggman", "Eggman"],
    ["gadget", "Gadget"],
    ["gamma", "Gamma"],
    ["lanolin", "Lanolin"],
    ["ray", "Ray"],
    ["shadow", "Shadow"],
    ["sonic", "Sonic"],
    ["tails", "Tails"],
    ["tangle", "Tangle"],
    ["vector", "Vector"],
    ["whisper", "Whisper"],
]

oc = [
    ["quickstrike", "Quickstrike", "shadzydow"],
    ["sharp", "Sharp", "thesupershotgun"],
]


def flatten(character_list, column):
    l = []
    for c in character_list:
        l.append(c[column])
    return l


def setup(bot):
    bot.add_cog(Pet(bot))


class Pet(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    pet = SlashCommandGroup("pet", "give out pets to various furballs")

    @pet.command(description="pet a character from the canon")
    async def character(
        self,
        ctx: discord.ApplicationContext,
        who: Option(
            str,
            "Who do you want to pet?",
            choices=[
                OptionChoice(name=c, value=str(index))
                for index, c in enumerate(flatten(character, 1))
            ],
        ),
    ):
        """
        Command that sends a specified petting gif.
        """
        url_slug, pet_who = character[int(who)]
        embed = discord.Embed(
            title=f"{ctx.author.display_name} is petting {pet_who}!",
        )
        embed.set_image(
            url=f"https://raw.githubusercontent.com/Silver-Volt4/SilverBot/main/assets/pet/character/{url_slug}.gif"
        )
        await ctx.respond(embed=embed)

    @pet.command(description="pet a user-submitted original character")
    async def oc(
        self,
        ctx: discord.ApplicationContext,
        who: Option(
            str,
            "Who do you want to pet?",
            choices=[
                OptionChoice(name=c, value=str(index))
                for index, c in enumerate(flatten(oc, 1))
            ],
        ),
    ):
        """
        Command that sends a specified petting gif.
        """
        url_slug, pet_who, owner = oc[int(who)]
        embed = discord.Embed(
            title=f"{ctx.author.display_name} is petting {pet_who}!",
        )
        embed.set_image(
            url=f"https://raw.githubusercontent.com/Silver-Volt4/SilverBot/main/assets/pet/oc/{url_slug}.gif"
        )
        embed.set_footer(text=f"@{owner}'s Original Character. Added on request.")
        await ctx.respond(embed=embed)
