import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APPLICATION_ID")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
RESET_TOKEN = os.getenv("RESET_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='`',intents=intents)

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.event
async def on_message(message):
    print(message.content)
    if message.author == bot.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        print("message sent")


bot.run(RESET_TOKEN)

