import asyncio

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

from connection import keep_alive

keep_alive() #for hosting on render
load_dotenv()

APP_ID = os.getenv("APPLICATION_ID")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")


bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

async def main():
    async with bot:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"loaded cog {filename}")
        await bot.start(AUTH_TOKEN)

asyncio.run(main())

