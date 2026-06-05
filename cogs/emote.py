import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import re

SUPPORTED_FORMAT = {"image/png","image/jpeg","image/gif","image/webp"}
MAX_SIZE = 256 * 1024

class Emote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="import", description="/import name(emote name) image_url")
    @app_commands.checks.has_permissions(manage_emojis=True)
    async def import_emote(self, interaction: discord.Interaction, name:str,url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"image could not be fetched, status: {response.status}")
                    await interaction.response.send_message(f"image could not be fetched",ephemeral=True)
                    return
                image = await response.read()
        emote = await interaction.channel.guild.create_custom_emoji(name=name, image=image)
        await interaction.response.send_message(f"emote: {emote} added")


    @app_commands.command(name="copy",description="/copy name(emote name) desired_emote")
    @app_commands.checks.has_permissions(manage_emojis=True)
    async def copy(self, interaction: discord.Interaction, name: str, emote:str):
        match = re.match(r"<(a?):(\w+):(\d+)>", emote)
        if not match:
            await interaction.response.send_message("ERROR: PLEASE PROVIDE A VALID CUSTOM EMOTE",ephemeral=True)
            return

        ext = "png"
        if match.groups()[0] == "a":
            ext = "gif"
        emote_id = match.groups()[2]
        url = f"https://cdn.discordapp.com/emojis/{emote_id}.{ext}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Failed to grab image, response-status: {response.status}")
                    await interaction.response.send_message("ERROR: IMAGE COULD NOT BE FETCHED",ephemeral=True)
                    return
                else:
                    image = await response.read()
        emote = await interaction.guild.create_custom_emoji(name=name, image=image)
        await interaction.response.send_message(f"EMOTE: {emote} added")

async def setup(bot):
    await bot.add_cog(Emote(bot))