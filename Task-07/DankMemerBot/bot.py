# I wrote the code with proper explanation of what that part does..

import discord
from discord.ext import commands
import config
# Instead of putting token directly to the code, I stored it in a seperate file..

import asyncio

intents = discord.Intents.default()
# This creates the default permissions for the bot..

intents.message_content = True
# This allows the bot to read messages like !ping, !bounty, !shop..

intents.members = True
# Allows the bot to access server member information (needed for !trade @user and !raid @user)..

bot = commands.Bot(
    command_prefix=config.PREFIX,
    intents=intents
)

# This tells Discord that my command prefix is !, use the intents which we enabled.. 
# and when someone types !ping, the bot recognizes it as a command


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
# This runs once, when the bot connects to Discord..

async def load_extensions():
    await bot.load_extension("cogs.fun")
    await bot.load_extension("cogs.economy")
    await bot.load_extension("cogs.shop")
    await bot.load_extension("cogs.onepiece")
    await bot.load_extension("cogs.history")
async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.TOKEN)

asyncio.run(main())