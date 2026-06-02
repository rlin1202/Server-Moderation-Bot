import discord
from discord import app_commands
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        welcome_channel = await self.bot.fetch_channel(1499773897858486325)
        print(f"{member.name} has joined")
        msg = discord.Embed(
            title="Welcome to Tribe slapahoe",
            description=f"{member.mention} has arrived on tribe slapahoe"
        )
        msg.set_thumbnail(url=member.avatar.url)
        msg.set_footer(text="Enjoy your stay!")

        await welcome_channel.send(content=f"Welcome to tribe slapahoe {member.mention}", embed=msg)

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        welcome_channel = await self.bot.fetch_channel(1499773897858486325)
        print(f"{member.name} has left")
        msg = discord.Embed(
            title=f"Goodbye {member.name} :(",
            description=f"{member.name} has left tribe slapahoe"
        )
        msg.set_thumbnail(url=member.avatar.url)
        msg.set_footer(text="You will be missed!")

        await welcome_channel.send(content=f"Goodbye {member.mention}", embed=msg)

    @app_commands.command(name="hello",description="Hello!")
    async def hello(self,interaction:discord.Interaction):
        await interaction.channel.send("Hello!")

    @app_commands.command(name="dbtest",description="Test db connection")
    async def dbtest(self, ctx):
        version = await self.bot.db.fetchval("SELECT version();")
        await ctx.send(version)

async def setup (bot):
    await bot.add_cog(Welcome(bot))