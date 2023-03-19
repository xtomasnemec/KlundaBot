import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands import Option
import os
import random
import datetime

from util.urlencode import urlencode
from util.error_message import apologize
from util.qrcode import generate_qr_code
from util.fetch import fetch_json

owm_api_key = os.environ.get("owm_api_key")


def setup(bot: discord.Bot):
    bot.add_cog(Util(bot))


class Util(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    util = SlashCommandGroup("util", "Miscellaneous utility commands")

    @util.command(description="Give a random number from a range")
    async def rand(
        self,
        ctx,
        min: Option(int, "The minimum number"),
        max: Option(int, "The maximum number"),
    ):
        await ctx.respond(random.randint(min, max))

    @util.command(description="Generate a QR code from a piece of text")
    async def qr(self, ctx, text: Option(str, "The text to encode")):
        qr_code = generate_qr_code(text)
        await ctx.send(
            f"👀 QR code requested by {ctx.author.name}", file=discord.File(qr_code.name)
        )
        await ctx.respond("✅ QR code generated.", ephemeral=True)

    @util.command(description="Search for a term using DuckDuckGo")
    async def ddg(self, ctx, term: Option(str, "The term to search for")):
        res = await fetch_json(
            f"https://api.duckduckgo.com/?q={urlencode(term)}&format=json"
        )

        if not (res["AbstractText"] == ""):
            embed = discord.Embed(
                title=res["Heading"],
                description=res["AbstractText"],
                url=res["AbstractURL"],
            )
            embed.set_footer(text="SilvBot")
            await ctx.respond(embed=embed)
        else:
            await apologize(ctx, "Aww, there are no results for that search.")

    @util.command(description="Learn new English words with UrbanDictionary")
    async def urban(self, ctx, word: Option(str, "The word to look up")):
        res = await fetch_json(
            f"http://api.urbandictionary.com/v0/define?term={urlencode(word)}"
        )

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

    @util.command(description="Get the weather for a location")
    async def weather(
        self, ctx, location: Option(str, "The location to get the weather for")
    ):
        weather = await fetch_json(
            f"https://api.openweathermap.org/data/2.5/weather?q={urlencode(location)}&appid={owm_api_key}"
        )
        error_code = weather["cod"]

        if error_code == "404":
            await apologize(ctx, "That city doesn't seem to exist.")
        else:
            condition = weather["weather"][0]["main"]
            icon = weather["weather"][0]["icon"]
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

            embed.add_field(name="Condition", value=condition, inline=False)

            embed.add_field(
                name="Current Temperature",
                value="{} °C\n{} °F".format(
                    round(temperatures["temp"] - 273.15),
                    round((temperatures["temp"] - 273.15) * 1.8 + 32),
                ),
                inline=True,
            )

            embed.add_field(
                name="Feels Like",
                value="{} °C\n{} °F".format(
                    round(temperatures["feels_like"] - 273.15),
                    round((temperatures["feels_like"] - 273.15) * 1.8 + 32),
                ),
                inline=True,
            )

            embed.add_field(
                name="Min/Max Temperature",
                value="{} - {} °C\n{} - {} °F".format(
                    round(temperatures["temp_min"] - 273.15),
                    round(temperatures["temp_max"] - 273.15),
                    round((temperatures["temp_min"] - 273.15) * 1.8 + 32),
                    round((temperatures["temp_max"] - 273.15) * 1.8 + 32),
                ),
                inline=True,
            )

            embed.add_field(
                name="Sunrise & Sunset",
                value="☀ {}\n🌙 {}".format(sunrise, sunset),
                inline=False,
            )

            embed.set_thumbnail(url=f"http://openweathermap.org/img/w/{icon}.png")

            embed.set_footer(text="SilvBot")
            await ctx.respond(embed=embed)

    @util.command(description="Check Silver's reaction time")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! {self.bot.latency}", ephemeral=True)

    @util.command(description="Flip a coin!")
    async def coin(self, ctx):
        await ctx.respond(
            "It's {}.".format(random.choice(["Heads", "Tails"])),
        )

    @util.command(description="Get the latest stuff from Reddit!")
    async def reddit(
        self, ctx, subreddit: Option(str, "The subreddit to get things from")
    ):
        if subreddit.startswith("r/"):
            subreddit = subreddit[2:]

        res = await fetch_json(
            f"https://api.reddit.com/r/{urlencode(subreddit)}/hot?limit=100&raw_json=1"
        )

        count = int(res["data"]["dist"])
        if count == 0:
            await apologize(ctx, "No results found... Does the subreddit exist?")
            return

        post = random.randint(0, count - 1)
        embed = discord.Embed(
            title=res["data"]["children"][post]["data"]["title"][0:256],
            description="by " + res["data"]["children"][post]["data"]["author"],
            url="https://reddit.com"
            + res["data"]["children"][post]["data"]["permalink"],
        )
        check = None
        try:
            check = res["data"]["children"][post]["data"]["preview"]["images"][0][
                "source"
            ]["url"]
        except:
            pass

        if check:
            embed.set_image(url=check)
        embed.set_footer(text="SilvBot")

        await ctx.respond(embed=embed)

    @util.command(description="Search for a word's definition")
    async def define(self, ctx, word):
        res = await fetch_json(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{urlencode(word)}"
        )

        if "title" in res:
            if res["title"] == "No Definitions Found":
                await apologize(ctx, "No definitions found...")
                return

        embeds = []
        for defn in res:
            embed = discord.Embed(title=defn["word"])
            for i, meaning in enumerate(defn["meanings"]):
                embed.add_field(
                    name=f"Meaning #{i+1} | **{meaning['partOfSpeech']}**",
                    value="\n".join(
                        ["• " + d["definition"] for d in meaning["definitions"]]
                    ),
                )
            embeds.append(embed)

        await ctx.respond("", embeds=embeds)
