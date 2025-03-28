"""
manage.py
Slash Commands that are meant to be used by whoever is hosting the bot.
"""

import os

import aiohttp
from discord import (
    Cog,
    ApplicationContext,
    DiscordException,
    ExtensionNotLoaded,
    ExtensionNotFound,
    Bot,
    Option,
    SlashCommandGroup, Embed,
)
from discord.ext.commands import NotOwner, is_owner

import silverbot
from db.pet import Character
from utils import repo, embeds
from utils.embeds import error_soft

admin_guild_id = int(os.environ.get("admin_guild_id", "0"))


def setup(bot):
    """
    Code to run on cog import.
    """
    bot.add_cog(Manage(bot))


class Manage(Cog):
    """
    Slash Commands that are meant to be used by whoever is hosting the bot.
    They are only available from one (presumably private) server.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    admin = SlashCommandGroup(
        "admin",
        "Commands for the bot's owner.",
        checks=[is_owner().predicate],
        guild_ids=[admin_guild_id],
    )

    def reload_cogs(self):
        for cog in silverbot.commands.list():
            try:
                self.bot.unload_extension(f"commands.{cog}")
            except (ExtensionNotLoaded, ExtensionNotFound):
                pass

        for cog in silverbot.commands.list():
            self.bot.load_extension(f"commands.{cog}")

    @admin.command(description="Reload the bot's extensions")
    async def reload(self, ctx: ApplicationContext):
        """
        Reloads extensions.
        """
        self.reload_cogs()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(descriptioon="Sync commands to a guild")
    async def sync(self, ctx: ApplicationContext):
        """
        Syncs all commands with Discord.
        """
        await self.bot.sync_commands()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(descriptioon="Sync commands to a guild")
    async def refreshall(self, ctx: ApplicationContext):
        """
        Reload and then sync.
        """
        self.reload_cogs()
        await self.bot.sync_commands()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(descriptioon="Add a pet command")
    async def addpet(
            self,
            ctx: ApplicationContext,
            gifname: Option(str, "GIF filename"),
            name: Option(str, "Character name"),
            is_oc: Option(bool, "Whether this is an OC"),
            owner: Option(str, "Owner of this OC (if applicable)", required=False),
            url: Option(
                str, "Image URL to download and automatically commit", required=False
            ),
    ):
        if is_oc and not owner:
            await ctx.respond(
                "❌ An owner must be supplied if adding an OC", ephemeral=True
            )
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
        self.bot.unload_extension("pet")
        self.bot.load_extension("pet")
        await self.bot.sync_commands()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(description="Update from GitHub")
    async def pull(self, ctx: ApplicationContext):
        """
        Update from GitHub.
        """
        await ctx.defer(ephemeral=True)
        repo.update()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(description="Dump info")
    async def dump(self, ctx: ApplicationContext):
        guild_embed = embeds.base(Embed(
            title="Guilds"
        ))
        for (i, guild) in enumerate(self.bot.guilds):
            guild_embed.add_field(name=f"{i + 1}) {guild.name}", value=f"{guild.member_count} members")
        await ctx.respond(embeds=[guild_embed], ephemeral=True)

    @Cog.listener()
    async def on_application_command_error(
            self, ctx: ApplicationContext, error: DiscordException
    ):
        """
        Handler for errors (to tell a user they can't use the bot).
        """
        if isinstance(error, NotOwner):
            ctx.options = {"handled": True}
            await ctx.respond(embed=error_soft("You can't use that command."))
