import aiohttp
import random
from discord.ext import commands


class OnePiece(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logpose(self, ctx):
        url = "https://api.api-onepiece.com/v2/characters/en"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:

                    if response.status != 200:
                        await ctx.send("❌ The Log Pose is malfunctioning!")
                        return

                    characters = await response.json()

            character = random.choice(characters)

            message = (
                "🧭 **LOG POSE ACTIVATED!** 🧭\n\n"
                f"🏴‍☠️ **Pirate:** {character['name']}\n"
                f"💰 **Bounty:** {character['bounty']}\n"
                f"👥 **Crew:** {character['crew']['name']}\n"
            )

            fruit = character.get("fruit")

            if fruit:
                message += (
                    f"🍈 **Devil Fruit:** {fruit['name']}\n"
                    f"✨ **Power:** {fruit['description']}\n"
                )
            else:
                message += "🍈 **Devil Fruit:** None known\n"

            await ctx.send(message)

        except Exception as error:
            print(f"❌ LOG POSE ERROR: {error}")
            await ctx.send("❌ The Log Pose couldn't find its way through the Grand Line.")


async def setup(bot):
    await bot.add_cog(OnePiece(bot))
    print("✅ One Piece cog loaded!")