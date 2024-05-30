"""
util.py
Commands that represent useful tools.
"""
import datetime
import random
import os

import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.commands import Option

from utils.urlencode import urlencode
from utils.error_message import apologize
from utils.qrcode import generate_qr_code
from utils.fetch import fetch_json
from utils.unit_conversions import to_celsius, to_fahrenheit

owm_api_key = os.environ.get("owm_api_key")


def setup(bot: discord.Bot):
    """
    Code to run on cog import.
    """
    bot.add_cog(Util(bot))


class Util(commands.Cog):
    """
    Commands that represent useful tools.
    """

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    util = SlashCommandGroup("util", "Miscellaneous utility commands")

    @util.command(description="Give a random number from a range")
    async def rand(
        self,
        ctx: discord.ApplicationContext,
        min_n: Option(int, "The minimum number"),
        max_n: Option(int, "The maximum number"),
    ):
        """
        Sends a random number in chat.
        """
        await ctx.respond(random.randint(min_n, max_n))

    @util.command(name="qr", description="Generate a QR code from a piece of text")
    async def qr_code(self, ctx: discord.ApplicationContext, text: Option(str, "The text to encode")):
        """
        Generates a QR code and sends it in chat as a message.
        """
        qr_code = generate_qr_code(text)
        file_name = qr_code.name
        await ctx.send(
            f"👀 QR code requested by {ctx.author.display_name}",
            file=discord.File(file_name),
        )
        await ctx.respond("✅ QR code generated.", ephemeral=True)
        os.remove(file_name)

    @util.command(description="Search for a term using DuckDuckGo")
    async def ddg(
        self,
        ctx: discord.ApplicationContext,
        term: Option(str, "The term to search for"),
    ):
        """
        Searches for a summary for a term and sends results.
        """
        search = await fetch_json(f"https://api.duckduckgo.com/?q={urlencode(term)}&format=json")

        if not search["AbstractText"] == "":
            embed = discord.Embed(
                title=search["Heading"],
                description=search["AbstractText"],
                url=search["AbstractURL"],
            )
            embed.set_footer(text="SilvBot")
            await ctx.respond(embed=embed)
        else:
            await apologize(ctx, "Aww, there are no results for that search.")

    @util.command(description="Learn new English words with UrbanDictionary")
    async def urban(self, ctx: discord.ApplicationContext, word: Option(str, "The word to look up")):
        """
        Searches a word with UrbanDictionary API and sends the result.
        """
        urban_def = await fetch_json(f"http://api.urbandictionary.com/v0/define?term={urlencode(word)}")

        if not len(urban_def["list"]) == 0:
            word = urban_def["list"][0]["word"]
            defi = urban_def["list"][0]["definition"]

            defi = defi.replace("[", "")
            defi = defi.replace("]", "")

            embed = discord.Embed(title=word, description=defi)
            embed.set_footer(text="SilvBot")

            await ctx.respond(embed=embed)
        else:
            await apologize(ctx, "Aww, there are no definitions for that word.")

    @util.command(description="Get the weather for a location")
    async def weather(
        self,
        ctx: discord.ApplicationContext,
        location: Option(str, "The location to get the weather for"),
    ):
        """
        Gets weather data for a location and sends it.
        """
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

            date = datetime.datetime.utcfromtimestamp(weather["dt"] + weather["timezone"]).strftime(
                "%A, %d %B %Y %I:%M %p"
            )

            sunrise = datetime.datetime.utcfromtimestamp(weather["sys"]["sunrise"] + weather["timezone"]).strftime(
                "%I:%M %p"
            )

            sunset = datetime.datetime.utcfromtimestamp(weather["sys"]["sunset"] + weather["timezone"]).strftime(
                "%I:%M %p"
            )

            embed = discord.Embed(
                description=f"retreived @ {date} (in local time)",
                title=f"The weather for {city_name}, {country_code}",
            )

            embed.add_field(name="Condition", value=condition, inline=False)

            embed.add_field(
                name="Current Temperature",
                value="{celsius} °C\n{fahrenheit} °F".format(
                    celsius=to_celsius(temperatures["temp"]),
                    fahrenheit=to_fahrenheit(temperatures["temp"]),
                ),
                inline=True,
            )

            embed.add_field(
                name="Feels Like",
                value="{celsius} °C\n{fahrenheit} °F".format(
                    celsius=to_celsius(temperatures["feels_like"]),
                    fahrenheit=to_fahrenheit(temperatures["feels_like"]),
                ),
                inline=True,
            )

            embed.add_field(
                name="Min/Max Temperature",
                value="{celsius_min} - {celsius_max} °C\n{fahrenheit_min} - {fahrenheit_max} °F".format(
                    celsius_min=to_celsius(temperatures["temp_min"]),
                    celsius_max=to_celsius(temperatures["temp_max"]),
                    fahrenheit_min=to_fahrenheit(temperatures["temp_min"]),
                    fahrenheit_max=to_fahrenheit(temperatures["temp_max"]),
                ),
                inline=True,
            )

            embed.add_field(
                name="Sunrise & Sunset",
                value=f"☀ {sunrise}\n🌙 {sunset}",
                inline=False,
            )

            embed.set_thumbnail(url=f"http://openweathermap.org/img/w/{icon}.png")

            embed.set_footer(text="SilvBot")
            await ctx.respond(embed=embed)

    @util.command(description="Check Silver's reaction time")
    async def ping(self, ctx: discord.ApplicationContext):
        """
        Sends bot latency.
        """
        await ctx.respond(f"Pong! {self.bot.latency}", ephemeral=True)

    @util.command(description="Flip a coin!")
    async def coin(self, ctx: discord.ApplicationContext):
        """
        Decides between two random values.
        """
        await ctx.respond(
            f"It's {random.choice(['Heads', 'Tails'])}.",
        )

    @util.command(description="Get the latest stuff from Reddit!")
    async def reddit(
        self,
        ctx: discord.ApplicationContext,
        subreddit: Option(str, "The subreddit to get things from"),
    ):
        """
        Downloads a random post from a subreddit and returns it.
        """
        if subreddit.startswith("r/"):
            subreddit = subreddit[2:]

        reddit_data = await fetch_json(f"https://api.reddit.com/r/{urlencode(subreddit)}/hot?limit=100&raw_json=1")

        count = int(reddit_data["data"]["dist"])
        if count == 0:
            await apologize(ctx, "No results found... Does the subreddit exist?")
            return

        post = random.randint(0, count - 1)
        embed = discord.Embed(
            title=reddit_data["data"]["children"][post]["data"]["title"][0:256],
            description="by " + reddit_data["data"]["children"][post]["data"]["author"],
            url="https://reddit.com" + reddit_data["data"]["children"][post]["data"]["permalink"],
        )
        check = None
        try:
            check = reddit_data["data"]["children"][post]["data"]["preview"]["images"][0]["source"]["url"]
        except KeyError:
            pass

        if check:
            embed.set_image(url=check)
        embed.set_footer(text="SilvBot")

        await ctx.respond(embed=embed)

    @util.command(description="Search for a word's definition")
    async def define(self, ctx: discord.ApplicationContext, word):
        """
        Searches for a word and sends its definiton in chat.
        """
        definition = await fetch_json(f"https://api.dictionaryapi.dev/api/v2/entries/en/{urlencode(word)}")

        if "title" in definition:
            if definition["title"] == "No Definitions Found":
                await apologize(ctx, "No definitions found...")
                return

        embeds = []
        for defn in definition:
            embed = discord.Embed(title=defn["word"])
            for i, meaning in enumerate(defn["meanings"]):
                embed.add_field(
                    name=f"Meaning #{i+1} | **{meaning['partOfSpeech']}**",
                    value="\n".join(["• " + d["definition"] for d in meaning["definitions"]]),
                )
            embeds.append(embed)

        await ctx.respond("", embeds=embeds)
