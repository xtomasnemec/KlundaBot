from discord import Embed, ApplicationContext


def base(embed: Embed, footer_additional: str | None = None) -> Embed:
    text = "SilverBot"
    if footer_additional:
        text += " | " + footer_additional
    embed.set_footer(text=text)
    return embed


async def send_soft_error(ctx: ApplicationContext, description: str):
    await ctx.respond(embed=error_soft(description), ephemeral=True)


def error_soft(description: str) -> Embed:
    return base(Embed(title=description, color=0xFF0000))


def error_critical(message: str) -> Embed:
    return base(
        Embed(
            title=":warning: An exception has occured.",
            description=f"Technical details: `{message}`\n"
            f"Please report this to the developer.",
            color=0xFF8C00,
        )
    )
