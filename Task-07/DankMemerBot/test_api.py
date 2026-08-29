import aiohttp
import asyncio


async def test_api():
    url = "https://api.api-onepiece.com/v2/characters/en"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)

            data = await response.json()

            print("Number of characters:", len(data))
            print("First character:")
            print(data[0])


asyncio.run(test_api())