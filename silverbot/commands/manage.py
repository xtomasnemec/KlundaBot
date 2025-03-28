"""
manage.py
Slash Commands that are meant to be used by whoever is hosting the bot.
"""

import os

import aiohttp
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands import Option

import silverbot
from db.pet import Character
from utils.embeds import error_soft
from utils import repo

admin_guild_id = int(os.environ.get("admin_guild_id", "0"))


def setup(bot):
    """
    Code to run on cog import.
    """
    bot.add_cog(Manage(bot))


class Manage(commands.Cog):
    """
    Slash Commands that are meant to be used by whoever is hosting the bot.
    They are only available from one (presumably private) server.
    """

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    admin = SlashCommandGroup(
        "admin",
        "Commands for the bot's owner.",
        checks=[commands.is_owner().predicate],
        guild_ids=[admin_guild_id],
    )

    def reload_cogs(self):
        for cog in silverbot.commands.list():
            try:
                self.bot.unload_extension(f"commands.{cog}")
            except (discord.ExtensionNotLoaded, discord.ExtensionNotFound):
                pass

        for cog in silverbot.commands.list():
            self.bot.load_extension(f"commands.{cog}")

    @admin.command(description="Reload the bot's extensions")
    async def reload(self, ctx: discord.ApplicationContext):
        """
        Reloads extensions.
        """
        self.reload_cogs()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(descriptioon="Sync commands to a guild")
    async def sync(self, ctx: discord.ApplicationContext):
        """
        Syncs all commands with Discord.
        """
        await self.bot.sync_commands()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(descriptioon="Sync commands to a guild")
    async def refreshall(self, ctx: discord.ApplicationContext):
        """
        Reload and then sync.
        """
        self.reload_cogs()
        await self.bot.sync_commands()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(descriptioon="Add a pet command")
    async def addpet(
            self,
            ctx: discord.ApplicationContext,
            gifname: Option(str, "GIF filename"),
            name: Option(str, "Character name"),
            is_oc: Option(bool, "Whether this is an OC"),
            owner: Option(str, "Owner of this OC (if applicable)", required=False),
            url: Option(str, "Image URL to download and automatically commit", required=False),
    ):
        if is_oc and not owner:
            await ctx.respond("❌ An owner must be supplied if adding an OC", ephemeral=True)
        if url:
            await ctx.defer(ephemeral=True)
            outfile = f'pet/{"oc" if is_oc else "character"}/{gifname}.gif'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        repo.add_asset(await resp.read(), outfile)

        Character.create(gif=gifname, name=name, is_oc=is_oc, owner=owner)
        # pylint: disable=protected-access
        self.bot._pending_application_commands = []
        self.bot.unload_extension("commands.pet")
        self.bot.load_extension("commands.pet")
        await self.bot.sync_commands()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(description="Update from GitHub")
    async def pull(self, ctx: discord.ApplicationContext):
        """
        Update from GitHub.
        """
        await ctx.defer(ephemeral=True)
        repo.update()
        await ctx.respond("✅ Done", ephemeral=True)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        """
        Handler for errors (to tell a user they can't use the bot).
        """
        if isinstance(error, commands.NotOwner):
            ctx.options = {"handled": True}
            await ctx.respond(embed=error_soft("You can't use that command."))
