import asyncio

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from connection import keep_alive
from util.db import create_pool

keep_alive() #for hosting on render
load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(),command_prefix="/")
        self.db = None

    #on start up we want to create that open connection and then go through the cogs folder and sync load all the commands


    async def setup_hook(self):
        self.db = await create_pool()
        # looks through the files in the cogs folder and returns a list of the filenames
        for filename in os.listdir("./cogs"):
            #looks for files that end in py and then loads the cogs ignoring the .py
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        #for slash commands that integrate with discord api, this locally syncs everything
        #global syncs take sometime up to an hour so we only use this for testing purposes
        guild = discord.Object(id=1387976713874444288)
        await self.tree.sync(guild=guild)

async def main():
    bot = DiscordBot()
    await bot.start(AUTH_TOKEN)

asyncio.run(main())