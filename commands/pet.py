"""
manage.py
Slash Commands that are meant to be used by whoever is hosting the bot.
"""
import asyncio
import os

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, OptionChoice, Option

from utils.error_message import apologize

requests_channel = int(os.environ.get("requests_channel", "0"))

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
    ["infinite", "Infinite"],
    ["kit", "Kit"],
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
    ["fick", "Fick", "damiancruz123"],
    ["sank", "Sank", "biggiemater23"],
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
        self.requests_channel: discord.GuildChannel = None

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

    @pet.command(description="request a character (canon or oc)")
    async def request(
        self,
        ctx: discord.ApplicationContext,
        who: Option(str, "Name of this character"),
        image: Option(
            str,
            "Image of this character. Must be a URL, e.g. DM the image to SilverBot and then copy the link",
        ),
    ):
        """
        Command that sends a specified petting gif.
        """
        if not self.requests_channel:
            self.requests_channel = await self.bot.fetch_channel(requests_channel)
        await self.requests_channel.send(
            f"new /pet request\nfrom: {ctx.author.name} {ctx.author.mention}\nname: {who}\n{image}"
        )
        await ctx.respond(
            "Your request was sent to me. I'll try to process it as fast as I can.\nDo not message me to speed things up. I have a life, too.\nIf we share a server, I will contact you when your character has been added.",
            ephemeral=True,
        )
