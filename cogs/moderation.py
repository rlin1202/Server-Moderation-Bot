import asyncio

import discord
from discord.ext import commands
from datetime import datetime, timedelta,timezone

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        general_channel = await self.bot.fetch_channel(1498406471744884776)
        print(f'logged in as {self.bot.user}')
        await general_channel.send("Hello, This is Ryan's bot. Please bare with him as he sucks at programming")

    @commands.command(aliases=["Kick"])
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, member: discord.Member, *, reason: str = "None provided"):
        if ctx.author.top_role > member.top_role:
            await member.kick(reason=reason)
            await ctx.send(f"{member} has been kicked, reason: {reason}")
        else:
            await ctx.send("ERROR: INAPPROPRIATE PERMISSIONS")

    @kick.error
    async def kick_error(self,ctx, error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.channel.send("ERROR: BOT IS MISSING PERMISSIONS")
        elif isinstance(error, discord.Forbidden):
            await ctx.channel.send("ERROR: USER DOES NOT HAVE PROPER PERMISSIONS")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("ERROR: SPECIFY MEMBER TO KICK")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.channel.send("ERROR: MEMBER NOT FOUND")
        else:
            await ctx.channel.send("ERROR: UNKNOWN")

    @commands.command(aliases=["Clear", "purge", "Purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx, amount: int):
        if amount < 1:
            await ctx.channel.send("ERROR: INVALID ARGUMENT")
            return
        cmd = ctx.channel.last_message
        await cmd.delete()

        old_time = datetime.now(timezone.utc) - timedelta(days=14)
        new_msg = []
        old_msg = []
        async for messages in ctx.channel.history(limit=amount):
            if messages.created_at < old_time:
                old_msg.append(messages)
            else:
                new_msg.append(messages)

        if new_msg:
            await ctx.channel.delete_messages(new_msg)

        for message in old_msg:
            await message.delete()
            await asyncio.sleep(1)

        confirmation_msg = await ctx.channel.send(f"{amount} messages have been deleted")
        await asyncio.sleep(3)
        await confirmation_msg.delete()

    @commands.command(aliases=["Timeout"])
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, amount: int = 30, unit: str = "seconds", *, reason: str = "None provided"):
        current_time = datetime.now(timezone.utc)
        max_time_out = current_time + timedelta(days=28)
        time_out_until = None
        if unit == "days" or unit == "d":
            time_out_until = current_time + timedelta(days=amount)
        elif unit == "hours" or unit == "hr":
            time_out_until = current_time + timedelta(hours=amount)
        elif unit == "minutes" or unit == "min" or unit == "m":
            time_out_until = current_time + timedelta(minutes=amount)
        elif unit == "seconds" or unit == "sec" or unit == "s":
            time_out_until = current_time + timedelta(seconds=amount)
        else:
            await ctx.send("ERROR: ARGUMENT NOT RECOGNIZED")
            return

        if time_out_until > max_time_out:
            await ctx.channel.send("ERROR: DURATION EXCEEDS 28 DAY MAXIMUM")
        elif ctx.author.top_role < member.top_role:
            await ctx.channel.send("ERROR: INAPPROPRIATE PERMISSIONS")
        else:
            await member.timeout(time_out_until)
            await ctx.send(f"{member} has been timed out for {amount} {unit}. Reason: {reason}")

    @timeout.error
    async def timeout_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send("ERROR: BOT IS MISSING PERMISSIONS")
        elif isinstance(error, discord.Forbidden):
            await ctx.channel.send("ERROR: USER DOES NOT HAVE PROPER PERMISSIONS")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("ERROR: SPECIFY MEMBER TO TIMEOUT")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.channel.send("ERROR: MEMBER NOT FOUND")
        else:
            await ctx.channel.send("ERROR: UNKNOWN")

async def setup(bot):
    await bot.add_cog(Moderation(bot))