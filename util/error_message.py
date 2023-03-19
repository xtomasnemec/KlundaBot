import discord


async def apologize(ctx, message):
    e = discord.Embed(description=":cry: " + message, color=0xff0000)
    await ctx.respond(embed=e, ephemeral=True)


async def panic(ctx, message):
    e = discord.Embed(description=":warning: " + message, color=0xff8c00)
    e.set_footer(
        text="This error is code related, and may not be your fault. Please report it.")
    await ctx.respond(embed=e, ephemeral=True)
