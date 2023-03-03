import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands import Option
import os
import random
import qrcode
import time
import json
import aiohttp
import datetime
from util.urlencode import urlencode

from util.error_message import apologize


def setup(bot: discord.Bot):
    bot.add_cog(Util(bot))


class Util(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    g = SlashCommandGroup("util", "Miscellaneous utility commands")

    @g.command(description="Give a random number from a range")
    async def rand(self, ctx, min: Option(int, "The minimum number"), max: Option(int, "The maximum number")):
        await ctx.respond(random.randint(min, max))

    @g.command(description="Generate a QR code from a piece of text")
    async def qr(self, ctx, text: Option(str, "The text to encode")):
        def qr_encode(text):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image()
            name = str(int(time.time())) + \
                str(random.randint(1, 100000)) + ".png"
            img.save(name)
            return name

        n = qr_encode(text)
        await ctx.send(f"👀 QR code requested by {ctx.author.name}", file=discord.File(n))
        await ctx.respond("✅ QR code generated.", ephemeral=True)
        os.remove(n)

    @g.command(description="Search for a term using DuckDuckGo")
    async def ddg(self, ctx, term: Option(str, "The term to search for")):
        async def get_ddg(term):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://api.duckduckgo.com/?q={urlencode(term)}&format=json&pretty=1',
                    headers={
                        'User-Agent': 'SilverBot for Discord'
                    }
                ) as response:
                    return json.loads(await response.text())
        res = await get_ddg(term)

        if not (res["AbstractText"] == ""):
            embed = discord.Embed(
                title=res["Heading"],
                description=res["AbstractText"],
                url=res["AbstractURL"]
            )
            embed.set_footer(text="SilvBot")
            await ctx.respond(embed=embed)
        else:
            await apologize(ctx, "Aww, there are no results for that search.")

    @g.command(description="Learn new English words with UrbanDictionary")
    async def urban(self, ctx, word: Option(str, "The word to look up")):
        async def get_urban(word):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'http://api.urbandictionary.com/v0/define?term={urlencode(word)}',
                    headers={
                        'Accept': 'application/json',
                        'User-Agent': 'SilverBot for Discord'
                    }
                ) as response:
                    return await response.json()
        res = await get_urban(word)

        if not (len(res["list"]) == 0):
            word = res["list"][0]["word"]
            defi = res["list"][0]["definition"]

            defi = defi.replace("[", "")
            defi = defi.replace("]", "")

            embed = discord.Embed(title=word, description=defi)
            embed.set_footer(text="SilvBot")

            await ctx.respond(embed=embed)
        else:
            await apologize(ctx, "Aww, there are no definitions for that word.")

    @g.command(description="Get the weather for a location")
    async def weather(
        self,
        ctx,
        location: Option(str, "The location to get the weather for")
    ):
        async def get_weather(location):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid=1ae200115efe68cbe99da9fce37951c5',
                    headers={
                        'Accept': 'application/json',
                        'User-Agent': 'SilverBot for Discord'
                    }
                ) as response:
                    return await response.json()

        location = urlencode(location)
        weather = await get_weather(location)
        print(weather)
        error_code = weather["cod"]

        if error_code == "404":
            await apologize(ctx, "That city doesn't seem to exist.")
            return
        else:
            condition = weather["weather"][0]["main"]
            icon = weather["weather"][0]["icon"]
            description = weather["weather"][0]["description"]
            temperatures = weather["main"]

            city_name = weather["name"]
            country_code = weather["sys"]["country"]

            date = datetime.datetime.utcfromtimestamp(
                weather["dt"] + weather["timezone"]
            ).strftime("%A, %d %B %Y %I:%M %p")

            sunrise = datetime.datetime.utcfromtimestamp(
                weather["sys"]["sunrise"] + weather["timezone"]
            ).strftime("%I:%M %p")

            sunset = datetime.datetime.utcfromtimestamp(
                weather["sys"]["sunset"] + weather["timezone"]
            ).strftime("%I:%M %p")

            embed = discord.Embed(
                description="retreived @ {} (in local time)".format(date),
                title="The weather for {}, {}".format(city_name, country_code),
            )

            embed.add_field(
                name="Condition",
                value=condition,
                inline=False
            )

            embed.add_field(
                name="Current Temperature",
                value="{} °C\n{} °F".format(
                    round(temperatures["temp"] - 273.15),
                    round((temperatures["temp"] - 273.15) * 1.8 + 32)
                ),
                inline=True
            )

            embed.add_field(
                name="Feels Like",
                value="{} °C\n{} °F".format(
                    round(temperatures["feels_like"] - 273.15),
                    round((temperatures["feels_like"] - 273.15) * 1.8 + 32)
                ),
                inline=True
            )

            embed.add_field(
                name="Min/Max Temperature",
                value="{} - {} °C\n{} - {} °F".format(
                    round(temperatures["temp_min"] - 273.15),
                    round(temperatures["temp_max"] - 273.15),
                    round((temperatures["temp_min"] - 273.15) * 1.8 + 32),
                    round((temperatures["temp_max"] - 273.15) * 1.8 + 32)
                ),
                inline=True
            )

            embed.add_field(
                name="Sunrise & Sunset",
                value="☀ {}\n🌙 {}".format(sunrise, sunset),
                inline=False
            )

            embed.set_thumbnail(
                url="http://openweathermap.org/img/w/{}".format(
                    icon + ".png")
            )

            embed.set_footer(text="SilvBot")

            await ctx.respond(embed=embed)

    @g.command(description="Check Silver's reaction time")
    async def ping(self, ctx):
        await ctx.respond(
            f"Pong! {self.bot.latency}",
            ephemeral=True
        )

    @g.command(description="Flip a coin!")
    async def coin(self, ctx):
        await ctx.respond(
            "It's {}.".format(random.choice(["Heads", "Tails"])),
        )

    @g.command(description="Get the latest stuff from Reddit!")
    async def reddit(
        self,
        ctx,
        subreddit: Option(str, "The subreddit to get things from")
    ):

        async def get_reddit(subreddit):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://api.reddit.com/r/{urlencode(subreddit)}/hot?limit=100&raw_json=1',
                    headers={
                        'Accept': 'application/json',
                        'User-Agent': 'SilverBot for Discord'
                    }
                ) as response:
                    return await response.json()

        if subreddit.startswith("r/"):
            subreddit = subreddit[2:]
        res = await get_reddit(subreddit)
        count = int(res["data"]["dist"])
        if count == 0:
            await apologize(ctx,"No results found... Does the subreddit exist?")
            return
        post = random.randint(0, count - 1)
        embed = discord.Embed(
            title=res["data"]["children"][post]["data"]["title"][0:256],
            description="by " +
            res["data"]["children"][post]["data"]["author"],
            url="https://reddit.com" +
            res["data"]["children"][post]["data"]["permalink"]
        )
        check = None
        try:
            check = res["data"]["children"][post]["data"]["preview"]["images"][0][
                "source"]["url"]
        except:
            pass

        if check:
            embed.set_image(url=check)
        embed.set_footer(text="SilvBot")

        await ctx.respond(embed=embed)

    @g.command(description="Search for a word's definition")
    async def define(self, ctx, word):
        async def get_dict(word):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://api.dictionaryapi.dev/api/v2/entries/en/{urlencode(word)}',
                    headers={
                        'User-Agent': 'SilverBot for Discord'
                    }
                ) as response:
                    return json.loads(await response.text())
        res = await get_dict(word)
        embeds = []

        if "title" in res:
            if res["title"] == "No Definitions Found":
                await apologize(ctx, "No definitions found...")
                return

        for defn in res:
            embed = discord.Embed(title=defn["word"])
            for i, meaning in enumerate(defn["meanings"]):
                embed.add_field(
                    name=f"Meaning #{i+1} | **{meaning['partOfSpeech']}**",
                    value="\n".join(["• " + d["definition"]
                                    for d in meaning["definitions"]])
                )
            embeds.append(embed)

        await ctx.respond("", embeds=embeds)
