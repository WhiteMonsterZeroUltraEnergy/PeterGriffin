import io
import aiohttp
import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="say", description="Bot repeats your message")
    async def say_command(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message("👍", ephemeral=True)
        await interaction.channel.send(message)

    @discord.app_commands.command(name="cat", description="Send a random cat picture 🐱")
    async def cat_command(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cataas.com/cat") as resp:
                if resp.status != 200:
                    await interaction.followup.send(f"`cataas.com` is not responding: {resp.status}")
                    return
                data = await resp.read()
        file = discord.File(fp=io.BytesIO(data), filename="cat.png")
        await interaction.followup.send(file=file)

    @discord.app_commands.command(name="catsays", description="Send a random cat saying text 🐱")
    async def cat_says_command(self, interaction: discord.Interaction, text: str = "%20"):
        await interaction.response.defer(thinking=False)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://cataas.com/cat/says/{text}") as resp:
                if resp.status != 200:
                    await interaction.followup.send(f"`cataas.com` is not responding: {resp.status}")
                    return
                data = await resp.read()
        file = discord.File(fp=io.BytesIO(data), filename="cat.png")
        await interaction.followup.send(file=file)

