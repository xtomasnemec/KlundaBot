import discord


def base(embed: discord.Embed, footer_additional: str | None = None) -> discord.Embed:
    text = "SilverBot"
    if footer_additional:
        text += " | " + footer_additional
    embed.set_footer(text=text)
    return embed


async def send_soft_error(ctx: discord.ApplicationContext, description: str):
    await ctx.respond(embed=error_soft(description), ephemeral=True)


def error_soft(description: str) -> discord.Embed:
    return base(discord.Embed(title=description, color=0xFF0000))


def error_critical(message: str) -> discord.Embed:
    return base(discord.Embed(
        title=":warning: An exception has occured.",
        description=f"Technical details: `{message}`\n"
                    f"Please report this to the developer.",
        color=0xFF8C00
    ))
