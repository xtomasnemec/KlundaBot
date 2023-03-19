import importlib
from util.error_message import apologize
import os
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands import Option

admin_guild_id = int(os.environ.get("admin_guild_id", "0"))


def setup(bot):
    bot.add_cog(Manage(bot))


class Manage(commands.Cog):
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
        self.bot._pending_application_commands = []
        for cog in [x[:-3] for x in os.listdir("commands") if x.endswith(".py")]:
            try:
                self.bot.unload_extension(f"commands.{cog}")
            except:
                pass

        for cog in [x[:-3] for x in os.listdir("commands") if x.endswith(".py")]:
            self.bot.load_extension(f"commands.{cog}")
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(description="Delete a message")
    async def delmsg(
        self, ctx: discord.ApplicationContext, id: Option(str, "ID to delete")
    ):
        await (await ctx.fetch_message(int(id))).delete()
        await ctx.respond("✅ Done", ephemeral=True)

    @admin.command(descriptioon="Sync commands to a guild")
    async def sync(self, ctx: discord.ApplicationContext):
        await ctx.respond("✅ Done", ephemeral=True)
        await self.bot.sync_commands()

    @admin.command(descriptioon="execute from file")
    async def exec(
        self,
        ctx: discord.ApplicationContext,
        cmd: Option(str, "command to run as defined in file"),
        args: Option(str, "semicolon separated"),
    ):
        import exec.exec

        importlib.reload(exec.exec)
        fun = getattr(exec.exec, cmd)
        await fun(ctx, args.split(";"))

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ):
        if isinstance(error, commands.NotOwner):
            ctx.options = {"handled": True}
            await apologize(ctx, "You can't use that command.")
