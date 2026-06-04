import asyncio
from encodings.aliases import aliases

import discord

from util.db import add_infraction,add_server_info
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta,timezone

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"logged in as {self.bot.user}")

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        guild_channel = guild.system_channel
        if not guild_channel:
            guild_channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),None)
        server_id = await add_server_info(self.bot.db,guild.id,guild_channel.id)
        print(f"joined server:{server_id}")

    #Add when user gets kicked we create a record in pg to keep track of information
    #generate a id for the case, user_id, moderator_id, type of action, reason, and set expires at to NULL
    @app_commands.command(name="kick", description="/kick @<user> reason(optional)")
    @commands.has_permissions(kick_members=True)
    async def kick(self,interaction: discord.Interaction, member: discord.Member, *, reason: str = "None provided"):
        if interaction.user.top_role > member.top_role:
            await member.kick(reason=reason)
            await interaction.channel.send(f"{member} has been kicked, reason: {reason}")
        else:
            await interaction.channel.send("ERROR: INAPPROPRIATE PERMISSIONS")

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

    @app_commands.command(name="clear",description="/clear <message amount>")
    @commands.has_permissions(manage_messages=True)
    async def clear(self,interaction, amount: int):
        if amount < 1:
            await interaction.channel.send("ERROR: INVALID ARGUMENT")
            return
        cmd = interaction.channel.last_message
        await cmd.delete()

        old_time = datetime.now(timezone.utc) - timedelta(days=14)
        new_msg = []
        old_msg = []
        async for messages in interaction.channel.history(limit=amount):
            if messages.created_at < old_time:
                old_msg.append(messages)
            else:
                new_msg.append(messages)

        if new_msg:
            await interaction.channel.delete_messages(new_msg)

        for message in old_msg:
            await message.delete()
            await asyncio.sleep(1)

        confirmation_msg = await interaction.channel.send(f"{amount} messages have been deleted")
        await asyncio.sleep(3)
        await confirmation_msg.delete()

    @app_commands.command(name="timeout",description="/timeout @<user> time(will default to 30 seconds) reason(optional)")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, amount: int = 30, unit: str = "seconds", *, reason: str = "None provided"):
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
            await interaction.channel.send("ERROR: ARGUMENT NOT RECOGNIZED")
            return

        if time_out_until > max_time_out:
            await interaction.channel.send("ERROR: DURATION EXCEEDS 28 DAY MAXIMUM")
        elif interaction.user.top_role < member.top_role:
            await interaction.channel.send("ERROR: INAPPROPRIATE PERMISSIONS")
        elif member.is_timed_out():
            await (interaction.channel.send("ERROR: MEMBER HAS ALREADY BEEN TIMED OUT"))
        else:
            await member.timeout(time_out_until)
            await interaction.channel.send(f"{member} has been timed out for {amount} {unit}. Reason: {reason}")

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

    @app_commands.command(name="ban",description="/ban @<user> reason(optional)")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "None provided"):
        if interaction.user.top_role > member.top_role:
            await member.ban(reason=reason,delete_message_days=7)
            await interaction.channel.send(f"{member} has been banned for {reason}")
        else:
            await interaction.channel.send("ERROR: INAPPROPRIATE PERMISSIONS")

    @app_commands.command(name="unban",description="/unban @<user> reason(optional)")
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member_id: str):

        user = await self.bot.fetch_user(int(member_id))
        print(f"unbanning {user}")
        await interaction.guild.unban(user)
        await interaction.channel.send(f"{user} has been unbanned")

    @app_commands.command(name="change_welcome",description="change default channel")
    @commands.has_permissions(manage_channels=True)
    async def change_welcome(self,interaction: discord.Interaction,channel_id: int):
        channel = await interaction.guild.fetch_channel(channel_id)

        await interaction.guild.edit(system_channel=channel)
        await interaction.channel.send(f"default channel has been changed to {channel.name}")



async def setup(bot):
    await bot.add_cog(Moderation(bot))