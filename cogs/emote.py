import discord
from discord.ext import commands
import aiohttp
import re


class Emote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="import", aliases=["Import"])
    @commands.has_permissions(manage_emojis=True)
    async def import_emote(self, ctx, name: str, url:str):
        image = None
        if url:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Failed to grab image, response-status: {response.status}")
                        ctx.send("ERROR: IMAGE COULD NOT BE FETCHED")
                        return
                    else:
                        image = response.read()
        emote = await ctx.guild.create_custom_emoji(name=name, image=image)
        await ctx.send(f"EMOTE: {emote} added")

    @commands.command(aliases=["Copy"])
    @commands.has_permissions(manage_emojis=True)
    async def copy(self, ctx, name: str, emote:str):
        match = re.match(r"<(a?):(\w+):(\d+)>", emote)
        if not match:
            await ctx.send("ERROR: PLEASE PROVIDE A VALID CUSTOM EMOTE")
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
                    await ctx.send("ERROR: IMAGE COULD NOT BE FETCHED")
                    return
                else:
                    image = await response.read()
        emote = await ctx.guild.create_custom_emoji(name=name, image=image)
        await ctx.send(f"EMOTE: {emote} added")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("ERROR: BOT IS MISSING PERMISSIONS")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("ERROR: USER DOES NOT HAVE PROPER PERMISSIONS")

async def setup(bot):
    await bot.add_cog(Emote(bot))