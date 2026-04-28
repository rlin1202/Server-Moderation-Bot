import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APPLICATION_ID")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def kenny(ctx):
    await ctx.send("Kenny is a pedophile")

@bot.event
async def on_member_join(member):
    general_channel =  await bot.fetch_channel(1387976715711545379)
    print(f"{member.name} has joined")
    msg = discord.Embed(
        title="Welcome to Tribe slapahoe",
        description=f"{member.name} has arrived on tribe slapahoe"
    )
    msg.set_thumbnail(url=member.avatar.url)
    msg.set_footer(text="Enjoy your stay!")

    await general_channel.send(embed=msg)

@bot.event
async def on_member_remove(member):
    general_channel = await bot.fetch_channel(1387976715711545379)
    print(f"{member.name} has left")
    msg = discord.Embed(
        title= f"Goodbye {member.name} :(",
        description=f"{member.name} has been banished from tribe slapahoe"
    )
    msg.set_thumbnail(url=member.avatar.url)
    msg.set_footer(text="You will be missed!")

    await general_channel.send(embed=msg)

bot.run(AUTH_TOKEN)

