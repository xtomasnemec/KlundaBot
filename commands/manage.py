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

    @admin.command(description="Reload the bot's extensions")
    async def reload(self, ctx: discord.ApplicationContext):
        """
        Reloads extensions.
        """
        for cog in [x[:-3] for x in os.listdir("commands") if x.endswith(".py")]:
            try:
                self.bot.unload_extension(f"commands.{cog}")
            except (discord.ExtensionNotLoaded, discord.ExtensionNotFound):
                pass

        # pylint: disable=protected-access
        self.bot._pending_application_commands = []

        for cog in [x[:-3] for x in os.listdir("commands") if x.endswith(".py")]:
            self.bot.load_extension(f"commands.{cog}")
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(descriptioon="Sync commands to a guild")
    async def sync(self, ctx: discord.ApplicationContext):
        """
        Syncs all commands with Discord.
        """
        await ctx.respond("✅ Done", ephemeral=True)
        await self.bot.sync_commands()
    
    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ):
        """
        Handler for errors (to tell a user they can't use the bot).
        """
        if isinstance(error, commands.NotOwner):
            ctx.options = {"handled": True}
            await apologize(ctx, "You can't use that command.")
