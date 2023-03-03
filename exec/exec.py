import discord

async def dl_stuff(ctx: discord.ApplicationContext, args):
    await ctx.defer()
    chnl = await ctx.guild.fetch_channel(1043386156911439922)
    async for m in ctx.channel.history():
        attachments = [m.url for m in m.attachments]
        for a in attachments:
            await chnl.send(a)
    await ctx.respond("done!!")
    print("done!!!")

async def testmsg(ctx: discord.ApplicationContext, args):
    await ctx.respond("done: " + "; ".join(), ephemeral=True)

async def perms(ctx: discord.ApplicationContext, args):
    print(ctx.channel.permissions_for(
        ctx.guild.get_member(ctx.bot.user.id)
    ).read_message_history)
    await ctx.respond("done", ephemeral=True)