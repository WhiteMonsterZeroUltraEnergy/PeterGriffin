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
        Reloads the specified cog using `reload_extension`,
        and synchronizes the commands tree without restarting the bot.

        :param ctx: The command invocation context.
        :param cog: The name of the cog to reload.
        """
        module_name = f"cogs.{cog}"
        try:
            await self.bot.reload_extension(module_name)
            await self.bot.sync_tree()
        except commands.ExtensionError as err:
            await ctx.reply(f"Error during reloading `{module_name}`:\n```py\n{err}```")
            logger.error(f"Error during reloading `{module_name}`", exc_info=err)
        else:
            await ctx.reply(f"Cog `{module_name}` has been successfully reloaded.")
            logger.info(f"Cog {module_name} reloaded by {ctx.author.id}.")

    @commands.command()
    @commands.is_owner()
    async def reload_all_cogs(self, ctx: commands.Context):
        """
        Reloads all currently loaded cogs from the `./cogs/` directory,
        and synchronizes the application commands tree without restarting the bot.

        :param ctx: The command invocation context.
        """
        for cog_name in list(self.bot.cogs.keys()):
            module_name = f"cogs.{cog_name.lower()}"
            try:
                await self.bot.reload_extension(module_name)
                await self.bot.sync_tree()
            except commands.ExtensionError as err:
                await ctx.reply(f"Error during reloading `{module_name}`:\n```py\n{err}```")
                logger.error(f"Error during reloading `{module_name}`", exc_info=err)
            else:
                await ctx.reply(f"The `./cogs/` directory has been reloaded, `{self.bot.config.cogs_count}` cogs.")
                logger.info(f"The `./cogs/` directory has been reloaded by {ctx.author.id}.")

    @commands.command()
    @commands.is_owner()
    async def load_cog(self, ctx: commands.Context, cog: str):
        """
        Loads the specified cog into the bot, registers it in the database,
        and synchronizes the application commands tree without restarting the bot.

        :param ctx: The command invocation context.
        :param cog: The name of the cog (without the 'cogs.' prefix) to load.
        """
        module_name = f"cogs.{cog}"
        try:
            await self.bot.load_extension(module_name)
            await self.bot.register_cog_in_db(module_name)
            await self.bot.sync_tree()
        except commands.ExtensionError as err:
            await ctx.reply(f"Error during loading `{module_name}`:\n```py\n{err}```")
            logger.error(f"Error during loading `{module_name}`", exc_info=err)
        else:
            await ctx.reply(f"Cog `{module_name}` has been successfully loaded.")
            logger.info(f"Cog {module_name} loaded by {ctx.author.id}.")

    @commands.command()
    @commands.is_owner()
    async def unload_cog(self, ctx: commands.Context, cog: str):
        """
        Unloads the specified cog from bot runtime, removes it from the database,
        and syncs the application commands tree.

        :arg ctx: The command invocation context.
        :arg cog: The name of the cog (without the 'cogs.' prefix) to unload.
        """
        module_name = f"cogs.{cog}"
        try:
            await self.bot.unload_extension(module_name)
            await self.bot.unregister_cog_in_db(module_name)
            await self.bot.sync_tree()
        except commands.ExtensionError as err:
            await ctx.reply(f"Error when disabling `{module_name}`:\n```py\n{err}```")
            logger.error(f"Error when disabling `{module_name}`", exc_info=err)
        else:
            await ctx.reply(f"Cog `{module_name}` has been successfully unloaded.")
            logger.info(f"Cog {module_name} has been successfully unloaded by {ctx.author.id}")

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
        embed.add_field(name="Commands:", value=f"`{self.bot.config.slash_commands_count}`", inline=True)
        embed.add_field(name="Version discord.py:", value=f"`{discord.__version__}`", inline=False)
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

    @commands.command()
    @commands.is_owner()
    async def list_cogs(self, ctx: commands.Context):
        """Displays all currently loaded cogs."""
        cogs = list(self.bot.cogs.keys())
        embed = Embed(
            title="Loaded Cogs",
            color=discord.Color.blue(),
            description="\n".join([f"`- {cog.lower()}`" for cog in cogs]),
        )
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        query = "INSERT INTO guilds (guild_id) VALUES ($1) ON CONFLICT DO NOTHING;"
        try:
            await self.bot.db.execute(query, guild.id)
        except Exception as err:
            logger.error(f"Postgresql: Failed to insert guild: {err}", exc_info=True)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        query = "DELETE FROM guilds WHERE guild_id = $1;"
        try:
            await self.bot.db.execute(query, guild.id)
        except Exception as err:
            logger.error(f"Postgresql: Failed to remove guild: {err}", exc_info=True)

    #
    # discord.errors.Forbidden: 403 Forbidden (error code: 50001): Missing Access
    #
    #@commands.Cog.listener()
    #async def on_guild_join(self, guild):
    #    system_channel = guild.system_channel
    #    if system_channel is not None:
    #        embed = Embed(
    #            title=f"**Rodacy!**",
    #            description=f"Przybywam do was jako syn tej ziemi, tego narodu, a zarazem, z niezbadanych wyroków Opatrzności, jako następca św. Piotra: na tej właśnie rzymskiej stolicy.\nDziękuję wam, żeście mnie zaprosili.\nWitam w duchu i obejmuję sercem każdego człowieka żyjącego na polskiej ziemi.",
    #            color=discord.Color.green(),
    #            timestamp=discord.utils.utcnow(),
    #            url="https://github.com/WhiteMonsterZeroUltraEnergy/PeterGriffin"
    #        )
    #        embed.set_footer(text=f"{self.bot.user}")
    #        await system_channel.send(embed=embed)
    #
    #
    #@commands.Cog.listener()
    #async def on_guild_remove(self, guild):
    #    system_channel = guild.system_channel
    #    if system_channel is not None:
    #        await system_channel.send("Goodbye")
