import discord
import os

from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APPLICATION_ID")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
RESET_TOKEN = os.getenv("RESET_TOKEN")

