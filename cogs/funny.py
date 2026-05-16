import random

import discord
from discord.ext import commands

caleb = 369867812942118933
kennu = 541452192046120981
cat = 404070206835785729
ryan = 612043297510129702
christian = 485842835027787818
kevin = 301037329651597321


class Funny(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=["Hello"])
    async def hello(self,ctx):
        message = None
        if ctx.author.id == caleb:
            message = "**What is up wiggers, chiggers, and ni-**"
        elif ctx.author.id == kennu:
            message = f"{ctx.author.mention} **stop throwing my elo**"
        elif ctx.author.id == cat:
            message = "**You're short**"
        elif ctx.author.id == ryan:
            message = "**Fuck you**"
        elif ctx.author.id == christian:
            message = "Can a nigga borrow a fry"
        elif ctx.author.id == kevin:
            message = "Can you spot me some food pls"
        else:
            message = "Hello!"

        await ctx.send(message)

    @commands.command(aliases=["Kenny"])
    async def kenny(self,ctx):
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

async def setup(bot):
    await bot.add_cog(Funny(bot))