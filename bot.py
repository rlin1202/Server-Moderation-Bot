import asyncio

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from util.db import create_pool

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

"""
DiscordBot inherits from commands.Bot
supports both prefix and slash commands

Attributes: 
    db = async postgres connections - declared before cogs are loaded to ensure db is available when cogs are registered
"""
class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members, intents.guilds, intents.bans = True
        super().__init__(intents=intents, command_prefix="!")
        self.db = None
    """
    Function initiates immediately after bot is logged in. After bot is logged in the function loads the cogs and 
    establishes a db connection.
    """
    async def setup_hook(self):
        self.db = await create_pool()
        # looks through the files in the cogs folder and returns a list of the filenames
        for filename in os.listdir("./cogs"):
            #looks for files that end in py and then loads the cogs ignoring the .py
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        #for slash commands that integrate with discord api, this locally syncs everything
        #global syncs take sometime up to an hour so we only use this for testing purposes
        #switch to self.tree.sync() for production
        
        guild = discord.Object(id=1387976713874444288)
        self.tree.copy_global_to(guild=guild)

        synced = await self.tree.sync(guild=guild)

async def main():
    bot = DiscordBot()
    async with bot:
        await bot.start(AUTH_TOKEN)

asyncio.run(main())