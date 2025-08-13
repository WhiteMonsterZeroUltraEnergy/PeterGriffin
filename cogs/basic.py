import discord
from discord.ext import commands


# noinspection PyUnresolvedReferences
class Basic(commands.Cog):
    """Basic sample bot commands."""

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Responds to ping.")
    async def ping(self, interaction: discord.Interaction):
        """Returns `Pong!` in response to /ping"""
        await interaction.response.send_message("Pong!", ephemeral=False)

    @discord.app_commands.command(name="prefix", description="Responds prefix command.")
    async def check_prefix(self, interaction: discord.Interaction):
        """Responds to prefix command."""
        await interaction.response.send_message(f"`{self.bot.config.prefix}`")


async def setup(bot):
    await bot.add_cog(Basic(bot))
