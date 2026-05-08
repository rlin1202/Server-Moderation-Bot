import discord
import os
import random
import asyncio
from datetime import datetime, timedelta,timezone

from discord.ext import commands
from dotenv import load_dotenv

from connection import keep_alive

keep_alive() #for hosting on render
load_dotenv()

APP_ID = os.getenv("APPLICATION_ID")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.command(aliases=["Hello"])
async def hello(ctx):
    message = None
    if ctx.author.id == 369867812942118933:
        message = "What is up wiggers, chiggers, and ni-"
    elif ctx.author.id == 541452192046120981:
        message = f"{ctx.author.mention} stop throwing my elo"
    elif ctx.author.id == 404070206835785729:
        message = "You're short"
    elif ctx.author.id == 612043297510129702:
        message = "Fuck you"
    else:
        message = "Hello!"
    await ctx.send(message)

@bot.command(aliases=["Kenny"])
async def kenny(ctx):
    kennu = await ctx.guild.fetch_member(541452192046120981)
    message = None
    temp = random.randint(1, 3)
    if temp == 3:
        message = f"{kennu.mention} is a pedophile"
    elif temp == 2:
        message = f"{kennu.mention} stop throwing my elo"

    await ctx.send(message)

#moderation commands
@bot.command(aliases=["Kick"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *,reason=None):
    if ctx.author.top_role > member.top_role:
        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked, reason: {reason}")
    else:
        await ctx.send("ERROR: INAPPROPRIATE PERMISSIONS")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, (commands.MissingPermissions,discord.Forbidden)):
        await ctx.channel.send("ERROR: MISSING PERMISSIONS")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("ERROR: SPECIFY MEMBER TO KICK")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.channel.send("ERROR: MEMBER NOT FOUND")
    else:
        await ctx.channel.send("ERROR: UNKNOWN")

@bot.command(aliases=["Clear"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    cmd = ctx.channel.last_message
    await cmd.delete()

    old_time = datetime.now(timezone.utc) - timedelta(days=14)
    new_msg = []
    old_msg =[]
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

#user join and leave
@bot.event
async def on_member_join(member):
    general_channel =  await bot.fetch_channel(1499773897858486325)
    print(f"{member.name} has joined")
    msg = discord.Embed(
        title="Welcome to Tribe slapahoe",
        description=f"{member.mention} has arrived on tribe slapahoe"
    )
    msg.set_thumbnail(url=member.avatar.url)
    msg.set_footer(text="Enjoy your stay!")

    await general_channel.send(content=f"Welcome to tribe slapahoe {member.mention}",embed=msg)

@bot.event
async def on_member_remove(member):
    general_channel = await bot.fetch_channel(1499773897858486325)
    print(f"{member.name} has left")
    msg = discord.Embed(
        title= f"Goodbye {member.name} :(",
        description=f"{member.name} has left tribe slapahoe"
    )
    msg.set_thumbnail(url=member.avatar.url)
    msg.set_footer(text="You will be missed!")

    await general_channel.send(content=f"Goodbye {member.mention}",embed=msg)

bot.run(AUTH_TOKEN)

