import time
import discord
from utils.logger import logger
from discord.ext import commands
from discord import SelectOption, Status, Embed


# noinspection PyUnresolvedReferences
class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload_cog(self, ctx: commands.Context, cog: str):
        """
        Reloads the specified module (cog), allowing dynamic code updates without having to restart the bot.
        This method uses `reload_extension` to first unload and then reload the selected module.

        :arg ctx: The context object of the command being invoked.
        :arg cog: The name of the cog to reload.
        """
        module_name = f"cogs.{cog}"
        try:
            await self.bot.reload_extension(module_name)
        except commands.ExtensionNotFound:
            await ctx.reply(f"Cog `{module_name}` not found.")
        except commands.ExtensionError as err:
            await ctx.reply(f"Error during reloading `{module_name}`:\n```py\n{err}```")
            logger.error(f"Error during reloading `{module_name}`", exc_info=err)
        else:
            await ctx.reply(f"Cog `{module_name}` has been successfully reloaded.")
            logger.info(f"Cog {module_name} reloaded by {ctx.author.id}.")
        self.bot.config.cogs_count = len(self.bot.cogs)

    @commands.command()
    @commands.is_owner()
    async def reload_all_cogs(self, ctx: commands.Context):
        """
        Reloads all currently loaded cogs found in the `./cogs/` directory.
        Enables dynamic refresh of all extensions without having to restart the application.
        It uses the `reload_extension` operation for each valid module.

        :arg ctx: The context object of the command being invoked.
        """
        for cog_name in list(self.bot.cogs.keys()):
            module_name = f"cogs.{cog_name.lower()}"
            try:
                await self.bot.reload_extension(module_name)
            except commands.ExtensionError as err:
                await ctx.reply(
                    f"Error during reloading `{module_name}`:\n```py\n{err}```"
                )
                logger.error(f"Error during reloading `{module_name}`", exc_info=err)
        self.bot.config.cogs_count = len(self.bot.cogs)
        await ctx.reply(
            f"The `./cogs/` directory has been reloaded, `{self.bot.config.cogs_count}` cogs."
        )
        logger.info(f"The `./cogs/` directory has been reloaded by {ctx.author.id}.")

    @commands.command()
    @commands.is_owner()
    async def load_cog(self, ctx: commands.Context, cog: str):
        """
        Loads the specified module (cog), allowing dynamic code updates without having to restart the bot.
        This method uses `load_extension` to load the selected module.

        :param ctx: The context object of the command being invoked.
        :param cog: The name of the cog to load.
        """
        module_name = f"cogs.{cog}"
        try:
            await self.bot.load_extension(module_name)
        except commands.ExtensionNotFound:
            await ctx.reply(f"Cog `{module_name}` not found.")
        except commands.ExtensionError as err:
            await ctx.reply(f"Error during loading `{module_name}`:\n```py\n{err}```")
            logger.error(f"Error during loading `{module_name}`", exc_info=err)
        else:
            await ctx.reply(f"Cog `{module_name}` has been successfully loaded.")
            logger.info(f"Cog {module_name} loaded by {ctx.author.id}.")
        self.bot.config.cogs_count = len(self.bot.cogs)

    @commands.command()
    @commands.is_owner()
    async def load_all_cogs(self, ctx: commands.Context):
        """
        Loads all modules (cogs) located in the `./cogs/` directory.
        Enables dynamic refresh of all extensions without having to restart the application.
        It uses the `load_extensions` (in DiscordBot class) method,
        which performs the `load_extension` operation for each valid module.

        :arg ctx: The context object of the command being invoked.
        """
        await self.bot.load_extensions()
        self.bot.config.cogs_count = len(self.bot.cogs)
        await ctx.reply(
            f"The `./cogs/` directory has been successfully loaded, `{self.bot.config.cogs_count}` cogs."
        )
        logger.info(f"Directory `./cogs/` loaded by {ctx.author.id}.")

    @commands.command()
    @commands.is_owner()
    async def unload_cog(self, ctx: commands.Context, cog: str):
        """
        Disables the specified module (cog).
        Allows you to dynamically remove a loaded module without having to restart the bot.
        This method uses `unload_extension` to unload the selected module.

        :arg ctx: The context object of the command being invoked.
        :arg cog: The name of the cog to unload.
        """
        module_name = f"cogs.{cog}"
        try:
            await self.bot.unload_extension(module_name)
        except commands.ExtensionNotFound:
            await ctx.reply(f"Cog `{module_name}` not found.")
        except commands.ExtensionError as err:
            await ctx.reply(f"Error when disabling `{module_name}`:\n```py\n{err}```")
            logger.error(f"Error when disabling `{module_name}`", exc_info=err)
        else:
            await ctx.reply(f"Cog `{module_name}` has been successfully unloaded.")
            logger.info(
                f"Cog {module_name} has been successfully unloaded by {ctx.author.id}"
            )
        self.bot.config.cogs_count = len(self.bot.cogs)

    @commands.command()
    @commands.is_owner()
    async def stats(self, ctx: commands.Context):
        """Displays a brief report"""
        uptime_seconds = round(time.time() - self.bot.config.start_timestamp)
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
        embed = Embed(
            title=f"Stats: {self.bot.user}",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
        )
        # fmt: off
        embed.add_field(name="Uptime:", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="Status:", value=f"`{self.bot.config.status}`", inline=True)
        embed.add_field(name="Cogs:", value=f"`{self.bot.config.cogs_count}`", inline=True)
        embed.add_field(name="Version discord.py:", value=f"`{discord.__version__}`", inline=True)
        embed.set_footer(text=f"{self.bot.user}")
        # fmt: on
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def change_presence_status(self, ctx: commands.Context):
        """
        Change the status of the bot via the selection menu
        Displays a dropdown menu for changing the bot's status.
        """

        # noinspection PyUnresolvedReferences
        class Select(discord.ui.Select):
            def __init__(self):
                options = [
                    SelectOption(
                        label="Available",
                        value="online",
                        description="Bot visible as Online",
                        emoji="<:ONLINE:1392593685035880478>",
                    ),
                    SelectOption(
                        label="Be right back",
                        value="idle",
                        description="Bot as Idle",
                        emoji="<:IDLE:1392593663724490792>",
                    ),
                    SelectOption(
                        label="Do not disturb",
                        value="dnd",
                        description="Bot as DND",
                        emoji="<:DND:1392593651841896550>",
                    ),
                    SelectOption(
                        label="Invisible",
                        value="invisible",
                        description="Bot as Offline",
                        emoji="<:OFFLINE:1392593675183325246>",
                    ),
                ]
                super().__init__(
                    placeholder="Select bot status...",
                    min_values=1,
                    max_values=1,
                    options=options,
                )

            async def callback(self, interaction: discord.Interaction):
                status_map = {
                    "online": Status.online,
                    "idle": Status.idle,
                    "dnd": Status.dnd,
                    "invisible": Status.invisible,
                }
                selected = status_map.get(self.values[0], Status.online)
                await self.view.bot.change_presence(status=selected)
                await interaction.response.edit_message(
                    content=f"Status changed to `{self.values[0]}`.", view=None
                )

        class SelectStatus(discord.ui.View):
            def __init__(self, bot):
                super().__init__()
                self.bot = bot
                self.add_item(Select())

        await ctx.reply(
            "Select the new status for the bot:", view=SelectStatus(self.bot)
        )
