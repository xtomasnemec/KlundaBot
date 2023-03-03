import importlib
from util.error_message import apologize
import os
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands import Option

def setup(bot):
    bot.add_cog(Admin(bot))


class Admin(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    g = SlashCommandGroup(
        "admin",
        "Commands for Volt to use.",
        checks=[
            commands.is_owner().predicate
        ]
    )

    @g.command(description="Reload the bot's extensions")
    async def reload(self, ctx):
        self.bot._pending_application_commands = []
        for cog in [x[:-3] for x in os.listdir("commands") if x.endswith(".py")]:
            try:
                self.bot.unload_extension(f"commands.{cog}")
            except:
                pass

        for cog in [x[:-3] for x in os.listdir("commands") if x.endswith(".py")]:
            self.bot.load_extension(f"commands.{cog}")
        await ctx.respond("✅ Done", ephemeral=True)

    @g.command(description="Delete a message")
    async def delmsg(self, ctx, id: Option(str, "ID to delete")):
        await (await ctx.fetch_message(int(id))).delete()
        await ctx.respond("✅ Done", ephemeral=True)

    @g.command(descriptioon="Sync commands to a guild")
    async def sync(self, ctx):
        await ctx.respond("✅ Done", ephemeral=True)
        await self.bot.sync_commands()

    @g.command(descriptioon="execute from file")
    async def exec(self, ctx, cmd: Option(str, "command to run as defined in file"), args: Option(str, "semicolon separated")):
        import exec.exec
        importlib.reload(exec.exec)
        fun = getattr(exec.exec, cmd)
        await fun(ctx,args.split(";"))

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.NotOwner):
            ctx.options = {"handled": True}
            await apologize(ctx, "You can't use that command.")
