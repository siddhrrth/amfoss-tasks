import database
from discord.ext import commands


class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def history(self, ctx):
        user_id = ctx.author.id

        records = database.get_history(user_id)

        if not records:
            await ctx.send("📜 Your pirate ledger is empty.")
            return

        message = "📜 **Pirate Ledger — Last 10 Transactions** 📜\n\n"

        for action, amount, description, created_at in records:
            if amount >= 0:
                amount_text = f"+{amount}"
            else:
                amount_text = str(amount)

            message += (
                f"**{action}** — `{amount_text} Berries`\n"
                f"📝 {description}\n"
                f"🕒 {created_at}\n\n"
            )

        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(History(bot))
    print("✅ History cog loaded!")