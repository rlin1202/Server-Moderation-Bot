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

caleb = 369867812942118933
kennu = 541452192046120981
cat = 404070206835785729
ryan = 612043297510129702
christian = 485842835027787818
kevin = 301037329651597321

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.event
async def on_ready():
    general_channel = await bot.fetch_channel(1498406471744884776)
    print(f'logged in as {bot.user}')
    await general_channel.send("Hello, This is Ryan's bot. Please bare with him as he sucks at programming")

@bot.command(aliases=["Hello"])
async def hello(ctx):
    message = None
    rand_num = random.randint(1,2)
    if rand_num == 1:
        message = "Hello!"
    else:
        if ctx.author.id == caleb:
            message = "What is up wiggers, chiggers, and ni-"
        elif ctx.author.id == kennu:
            message = f"{ctx.author.mention} stop throwing my elo"
        elif ctx.author.id == cat:
            message = "You're short"
        elif ctx.author.id == ryan:
            message = "Fuck you"
        elif ctx.author.id == christian:
            message = "Can a nigga borrow a fry"
        elif ctx.author.id == kevin:
            message = "Can you spot me some food pls"

    await ctx.send(message)

@bot.command(aliases=["Kenny"])
async def kenny(ctx):
    kennu = await ctx.guild.fetch_member(541452192046120981)
    message = None
    temp = random.randint(1, 5)
    if temp == 1:
        message = f"{kennu.mention} is a pedophile"
    elif temp == 2:
        message = f"{kennu.mention} stop throwing my elo"
    elif temp == 3:
        message = f"{kennu.mention} check your fire with civilians"
    elif temp == 4:
        message = f"{kennu.mention} is full extended in kids"
    elif temp == 5:
        message = f"{kennu.mention}: Epstein's #1 soldier"
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

@bot.command(aliases=["Clear","purge","Purge"])
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
    welcome_channel =  await bot.fetch_channel(1499773897858486325)
    print(f"{member.name} has joined")
    msg = discord.Embed(
        title="Welcome to Tribe slapahoe",
        description=f"{member.mention} has arrived on tribe slapahoe"
    )
    msg.set_thumbnail(url=member.avatar.url)
    msg.set_footer(text="Enjoy your stay!")

    await welcome_channel.send(content=f"Welcome to tribe slapahoe {member.mention}",embed=msg)

@bot.event
async def on_member_remove(member):
    welcome_channel = await bot.fetch_channel(1499773897858486325)
    print(f"{member.name} has left")
    msg = discord.Embed(
        title= f"Goodbye {member.name} :(",
        description=f"{member.name} has left tribe slapahoe"
    )
    msg.set_thumbnail(url=member.avatar.url)
    msg.set_footer(text="You will be missed!")

    await welcome_channel.send(content=f"Goodbye {member.mention}",embed=msg)

bot.run(AUTH_TOKEN)

