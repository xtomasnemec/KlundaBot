import discord


async def apologize(ctx: discord.ApplicationContext, message: str):
    e = discord.Embed(description=":cry: " + message, color=0xFF0000)
    await ctx.respond(embed=e, ephemeral=True)


async def panic(ctx: discord.ApplicationContext, message: str):
    e = discord.Embed(description=":warning: " + message, color=0xFF8C00)
    e.set_footer(
        text="This error is code related, and may not be your fault. Please report it."
    )
    await ctx.respond(embed=e, ephemeral=True)
