import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("🏴‍☠️ Pong!")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Ahoy {ctx.author.mention}! Welcome aboard! 🏴‍☠️")


async def setup(bot):
    await bot.add_cog(Fun(bot))