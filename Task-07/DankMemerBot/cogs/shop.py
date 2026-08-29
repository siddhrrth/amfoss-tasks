import json
import database
from discord.ext import commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        try:
            with open("data/shop.json", "r", encoding="utf-8") as file:
                items = json.load(file)

            message = "🛒 **Berry Broker's Shop** 🛒\n\n"

            for item in items:
                message += (
                    f"{item['emoji']} **{item['name']}**\n"
                    f"💰 Price: **{item['price']} Berries**\n"
                    f"✨ Effect: {item['effect']}\n\n"
                )

            await ctx.send(message)

        except Exception as error:
            print(f"❌ SHOP ERROR: {error}")
            await ctx.send("❌ The Berry Broker's shop is currently unavailable.")


    @commands.command()
    async def buy(self, ctx, *, item_name):
        with open("data/shop.json", "r", encoding="utf-8") as file:
            items = json.load(file)

        selected_item = None

        for item in items:
            if item["name"].lower() == item_name.lower():
                selected_item = item
                break

        if selected_item is None:
            await ctx.send("❌ That item does not exist in the shop.")
            return

        user_id = ctx.author.id
        price = selected_item["price"]

        balance = database.get_wallet(user_id)

        if balance < price:
            await ctx.send(
                f"❌ You don't have enough Berries!\n"
                f"💰 Required: **{price}**\n"
                f"💰 Your wallet: **{balance}**"
            )
            return

        database.update_wallet(user_id, balance - price)
        database.add_item(user_id, selected_item["name"])

        database.add_history(
            user_id,
            "BUY",
            -price,
            f"Bought {selected_item['name']}"
        )

        await ctx.send(
            f"🏴‍☠️ **Purchase successful!**\n"
            f"{selected_item['emoji']} You bought **{selected_item['name']}**\n"
            f"💰 Spent: **{price} Berries**\n"
            f"💰 Remaining: **{balance - price} Berries**"
        )
        
    @commands.command()
    async def inventory(self, ctx):
        user_id = ctx.author.id

        items = database.get_inventory(user_id)

        if not items:
            await ctx.send("🎒 Your inventory is empty.")
            return

        message = "🎒 **Your Pirate Inventory** 🎒\n\n"

        for item_name, quantity, active in items:
            status = "🟢 Active" if active else "🔴 Spent"

            message += (
                f"📦 **{item_name}**\n"
                f"🔢 Quantity: **{quantity}**\n"
                f"📊 Status: {status}\n\n"
            )

        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Shop(bot))
    print("✅ Shop cog loaded!")