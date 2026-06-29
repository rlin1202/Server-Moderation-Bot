import asyncio

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

    @app_commands.command(
        name="kick",
        description="kicks a user"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self,interaction: discord.Interaction, member: discord.Member, *, reason: str = "None provided"):
        member_id = member.id
        if interaction.user.top_role > member.top_role:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member} has been kicked, reason: {reason}")
            try:
                await add_infraction(
                    self.bot.db,
                    member_id,
                    interaction.guild.id,
                    interaction.user.id,
                    "KICK",
                    reason
                )
            except Exception as e:
                print(f"DB error: {e}")
        else:
            await interaction.response.send_message("ERROR: INAPPROPRIATE PERMISSIONS",ephemeral=True)


    @app_commands.command(name="clear",description="clears x amount of messages from a channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self,interaction, amount: int):
        if amount < 1:
            await interaction.response.send_message("ERROR: INVALID ARGUMENT",ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)

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

        await interaction.followup.send(f"{amount} messages have been deleted",ephemeral=True)

    @app_commands.command(
        name="timeout",
        description="times out a user for x amount of days, hours, minutes, or seconds"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, amount: int = 30, unit: str = "seconds", reason: str = "None provided"):
        if interaction.user.top_role < member.top_role:
            await interaction.response.send_message("ERROR: INAPPROPRIATE PERMISSIONS", ephemeral=True)
            return
        elif member.is_timed_out():
            await interaction.response.send_message("ERROR: MEMBER HAS ALREADY BEEN TIMED OUT", ephemeral=True)
            return

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
            await interaction.response.send_message("ERROR: ARGUMENT NOT RECOGNIZED", ephemeral=True)
            return

        if time_out_until > max_time_out:
            await interaction.response.send_message("ERROR: DURATION EXCEEDS 28 DAY MAXIMUM", ephemeral=True)
            return
        else:
            await interaction.response.defer()
            try:
                await member.timeout(time_out_until)
                await add_infraction(
                    self.bot.db,
                    member.id,
                    interaction.guild.id,
                    interaction.user.id,
                    "TIMEOUT",
                    reason,
                    time_out_until,
                    True
                )
                await interaction.followup.send(f"{member} has been timed out for {amount} {unit}. Reason: {reason}")
            except Exception as e:
                print(f"DB error: {e}")
                await interaction.followup.send("ERROR: SOMETHING WENT WRONG", ephemeral=True)

    @app_commands.command(
        name="ban",
        description="/bans a user either permanently or temporary for x amount of days or weeks"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, amount:int = None, unit:str = None, reason: str = "None provided"):
        ban_until = None
        member_id = member.id
        if interaction.user.top_role > member.top_role:
            if amount and unit:
                current_time = datetime.now(timezone.utc)
                if unit == "days" or unit == "d":
                    ban_until = current_time + timedelta(days=amount)
                elif unit == "weeks" or unit == "w":
                    ban_until = current_time + timedelta(weeks=amount)
            await interaction.response.defer()
            try:
                await member.ban(reason=reason,delete_message_seconds=604800)
                await add_infraction(
                    self.bot.db,
                    member_id,
                    interaction.guild.id,
                    interaction.user.id,
                    "BAN",
                    reason,
                    ban_until,
                    True
                )
                await interaction.followup.send(f"{member} has been banned for {reason}")
            except Exception as e:
                print(f"DB error: {e}")
                await interaction.followup.send("ERROR: SOMETHING WENT WRONG",ephemeral=True)
        else:
            await interaction.response.send_message("ERROR: INAPPROPRIATE PERMISSIONS",ephemeral=True)

    @app_commands.command(name="unban",description="unbans a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member_id: str):

        user = await self.bot.fetch_user(int(member_id))
        print(f"unbanning {user}")
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"{user} has been unbanned")

    @app_commands.command(name="change_welcome",description="changes default or welcome channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def change_welcome(self,interaction: discord.Interaction, channel: discord.TextChannel):

        await interaction.guild.edit(system_channel=channel)
        await interaction.response.send_message(f"default channel has been changed to {channel.name}")

        query = """
            UPDATE servers 
            SET welcome_channel = $1
            WHERE server_id = $2
        """

        await self.bot.db.execute(query,channel.id,interaction.guild.id)

    @app_commands.command(name="warn", description="issues the user a warning for behaving")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "None Provided"):
        if interaction.user.top_role > member.top_role:
            await add_infraction(
                self.bot.db,
                member.id,
                interaction.guild.id,
                interaction.user.id,
                "WARN",
                reason
            )
            await interaction.response.send_message(f"{member.mention} has been issues a warning! Reason: {reason}")
        else:
            await interaction.response.send_message("ERROR: INAPPROPRIATE PERMISSIONS", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))