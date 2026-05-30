import asyncio

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands
from connection import keep_alive
from util.db import create_pool

keep_alive() #for hosting on render
load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.all(),command_prefix="/")
        self.db = None

    async def setup_hook(self):
        self.db = await create_pool()
        for filename in os.listdir("./cogs"):
            if filename.endswith("py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        await self.tree.sync()

async def main():
    bot = DiscordBot()
    await bot.start(AUTH_TOKEN)

asyncio.run(main())