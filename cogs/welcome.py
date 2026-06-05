import discord
from discord import app_commands
from discord.ext import commands

from util.db import fetch_welcome_channel, add_server_info


class Welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"on_guild_join fired for {guild.name}")
        guild_channel = guild.system_channel
        print(f"system channel: {guild_channel}")
        if not guild_channel:
            guild_channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
        try:
            server_id = await add_server_info(self.bot.db, guild.id, guild_channel.id)
            print(f"joined server:{server_id}")
        except Exception as e:
            print(f"DB error: {e}")

    @commands.Cog.listener()
    async def on_member_join(self,member):
        server = member.guild
        channel_id = await fetch_welcome_channel(self.bot.db,server.id)
        welcome_channel = await self.bot.fetch_channel(channel_id)
        print(f"{member.name} has joined")
        msg = discord.Embed(
            title=f"Welcome to {server.name}",
            description=f"{member.mention} has arrived on tribe {server.name}"
        )
        msg.set_thumbnail(url=member.avatar.url)
        msg.set_footer(text="Enjoy your stay!")

        await welcome_channel.send(content=f"Welcome to {server.name} {member.mention}", embed=msg)
    
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        server = member.guild
        channel_id = await fetch_welcome_channel(self.bot.db, server.id)
        welcome_channel = await self.bot.fetch_channel(channel_id)

        print(f"{member.name} has left")
        msg = discord.Embed(
            title=f"Goodbye {member.name} :(",
            description=f"{member.name} has left tribe {server.name}"
        )
        msg.set_thumbnail(url=member.avatar.url)
        msg.set_footer(text="You will be missed!")

        await welcome_channel.send(content=f"Goodbye {member.mention}", embed=msg)

    @app_commands.command(name="hello",description="Hello!")
    async def hello(self, interaction: discord.Interaction):
        await (interaction.response.send_message("Hello!"))

    @app_commands.command(name="link", description="Provides link to invite bot")
    async def link(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://discord.com/oauth2/authorize?client_id=1493243323509375207",ephemeral=True)

    @app_commands.command(name="dbtest",description="Test db connection")
    async def dbtest(self, interaction: discord.Interaction):
        version = await self.bot.db.fetchval("SELECT version();")
        await interaction.response.send_message(version)

async def setup (bot):
    await bot.add_cog(Welcome(bot))