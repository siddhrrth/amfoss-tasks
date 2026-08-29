import discord
from discord.ext import commands
from datetime import datetime, timedelta
import database
import random


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bounty(self, ctx):
        balance = database.get_wallet(ctx.author.id)

        await ctx.send(
            f"🏴‍☠️ **{ctx.author.display_name}'s Bounty**\n"
            f"💰 Wallet: **{balance}** Berries"
        )

    @commands.command()
    async def setsail(self, ctx):
        user_id = ctx.author.id

        last_daily = database.get_last_daily(user_id)

        if last_daily is not None:
            last_daily = datetime.fromisoformat(last_daily)

            if datetime.now() - last_daily < timedelta(days=1):
                await ctx.send(
                    "❌ You have already claimed your daily Berries! "
                    "Come back later."
                )
                return

        balance = database.get_wallet(user_id)
        new_balance = balance + 300

        database.update_wallet(user_id, new_balance)
        database.update_last_daily(
            user_id,
            datetime.now().isoformat()
        )

        database.add_history(
            user_id,
            "DAILY",
            300,
            "Claimed daily Berries"
        )

        await ctx.send(
            f"🏴‍☠️ You set sail and earned **300 Berries!**\n"
            f"💰 Wallet: **{new_balance}** Berries"
        )

    @commands.command()
    async def trade(self, ctx, member: discord.Member, amount: int):
        # Prevent trading with yourself
        if member.id == ctx.author.id:
            await ctx.send("❌ You cannot trade with yourself!")
            return

        # Amount must be positive
        if amount <= 0:
            await ctx.send("❌ Enter a valid amount.")
            return

        sender_balance = database.get_wallet(ctx.author.id)

        # Check if sender has enough money
        if sender_balance < amount:
            await ctx.send("❌ You don't have enough Berries.")
            return

        # Transfer Berries
        database.add_wallet(ctx.author.id, -amount)
        database.add_wallet(member.id, amount)

        # Record transaction for sender
        database.add_history(
            ctx.author.id,
            "TRADE",
            -amount,
            f"Sent {amount} Berries to {member.display_name}"
        )

        # Record transaction for receiver
        database.add_history(
            member.id,
            "TRADE",
            amount,
            f"Received {amount} Berries from "
            f"{ctx.author.display_name}"
        )

        await ctx.send(
            f"🏴‍☠️ {ctx.author.mention} traded "
            f"**{amount} Berries** to {member.mention}!"
        )

    @commands.command()
    async def worstgeneration(self, ctx):
        top_users = database.get_top_users()

        if not top_users:
            await ctx.send("No pirates found!")
            return

        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

        message = "🏴‍☠️ **Worst Generation** 🏴‍☠️\n\n"

        for i, (user_id, wallet) in enumerate(top_users):
            user = self.bot.get_user(user_id)

            if user:
                name = user.display_name
            else:
                name = f"User {user_id}"

            message += (
                f"{medals[i]} **{name}** - "
                f"{wallet} Berries\n"
            )

        await ctx.send(message)

    @commands.command()
    async def raid(self, ctx, target: discord.Member):
        attacker_id = ctx.author.id
        target_id = target.id

        # Prevent self-raiding
        if attacker_id == target_id:
            await ctx.send("❌ You can't raid yourself!")
            return

        target_balance = database.get_wallet(target_id)

        # Target has nothing to steal
        if target_balance <= 0:
            await ctx.send(
                f"🏴‍☠️ **{target.display_name}** "
                f"has no Berries to raid!"
            )
            return

        # 50% chance of success
        success = random.random() < 0.5

        if not success:
            await ctx.send(
                f"⚔️ **RAID FAILED!**\n"
                f"🏴‍☠️ {target.display_name}'s crew "
                f"defended their treasure!"
            )
            return

        # Steal 20% of the target's wallet
        loot = max(1, int(target_balance * 0.20))

        stolen = database.raid_transfer(
            attacker_id,
            target_id,
            loot
        )

        # Record attacker's history
        database.add_history(
            attacker_id,
            "RAID",
            stolen,
            f"Raided {target.display_name}"
        )

        # Record target's history
        database.add_history(
            target_id,
            "RAID",
            -stolen,
            f"Was raided by {ctx.author.display_name}"
        )

        new_balance = database.get_wallet(attacker_id)

        await ctx.send(
            f"⚔️ **RAID SUCCESS!**\n"
            f"🏴‍☠️ **{ctx.author.display_name}** raided "
            f"**{target.display_name}**!\n"
            f"💰 Loot stolen: **{stolen} Berries**\n"
            f"💰 Your new wallet: **{new_balance} Berries**"
        )
        
async def setup(bot):
    await bot.add_cog(Economy(bot))
    print("✅ Economy cog loaded!")