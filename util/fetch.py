import aiohttp


async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={'Accept': 'application/json', 'User-Agent': 'SilverBot for Discord'}) as response:
            return await response.json(content_type=None)
