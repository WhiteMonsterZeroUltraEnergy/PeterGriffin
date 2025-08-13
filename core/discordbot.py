"""
File: discordant.py

Author: WhiteMonsterZeroUltraEnergy
Repository: https://github.com/WhiteMonsterZeroUltraEnergy/PeterGriffin
License: GPL v3

Description:
    The main module of the Discord bot, responsible for initializing the connection to the database and automatically loading and synchronizing modules (cogs).
"""

from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import CommandNotFound, Context
from core.database import Database
from utils.logger import logger
from utils.config import Config


class DiscordBot(commands.Bot):
    def __init__(self, config: Config, *args, **kwargs):
        intents = discord.Intents.default()
        if config.intents_payload is not None:
            intents.value = config.intents_payload
        bot_kwargs = {
            "command_prefix": config.prefix,
            "status": config.status,
            "owner_ids": config.owner_ids or None,
            "owner_id": None if config.owner_ids else config.owner_id,
            "allowed_mentions": config.allowed_mentions,
            "case_insensitive": config.case_insensitive,
            "strip_after_prefix": config.strip_after_prefix,
            "intents": intents,
            **kwargs,
        }
        super().__init__(*args, **bot_kwargs)

        self.config = config
        self.db = Database(
            host=config.psql_host,
            port=config.psql_port,
            database=config.psql_db_name,
            schema=config.psql_schema,
            user=config.psql_user,
            password=config.psql_password,
        )

    def __del__(self):
        logger.warning(f"Bot {self.user} is offline.")

    async def setup_hook(self):
        """The hook triggered when the bot starts is used to initialize extensions."""
        await self.load_extensions()

    async def on_ready(self):
        """Method called when the bot is ready to run (after fully loading)."""
        logger.info(
            f"Bot {self.user} is online. "
            f"Version used: discord.py {discord.__version__}"
        )

    async def on_connect(self):
        """Called after connecting to Discord (before full readiness `on_ready`)."""
        logger.warning(f"Bot {self.user} connected.")

    async def on_disconnect(self):
        """Called after losing connection to Discord."""
        logger.critical(f"Bot {self.user} disconnected.")

    async def load_extensions(self):
        """
        Automatically loads all modules (`cogs`) from the ./cogs/ directory and
        synchronizes application commands.
        """
        cogs_dir = Path("./cogs")
        if not cogs_dir.exists():
            logger.error(f"The {cogs_dir} directory does not exist.")
            return

        for module_path in Path(cogs_dir).iterdir():
            # Loading .py files (excluding __init__.py)
            if module_path.suffix == ".py" and module_path.name != "__init__.py":
                ext = f"cogs.{module_path.stem}"
            # Loading directories containing __init__.py
            elif module_path.is_dir() and (module_path / "__init__.py").exists():
                ext = f"cogs.{module_path.name}"
            # Skip mismatched files
            else:
                continue
            # Attempt to load module
            try:
                await self.load_extension(ext)
                logger.info(f"Module loaded: {ext}")
            except Exception as err:
                logger.error(f"Loading error {ext}: {err}", exc_info=True)
        # Synchronization of application commands (slash commands)
        try:
            synced = await self.tree.sync()
            self.config.slash_commands_count = len(synced)
            self.config.cogs_count = len(self.cogs)
            logger.info(f"Synced {self.config.cogs_count} cogs.")
            logger.info(
                f"Synchronized {self.config.slash_commands_count} application commands."
            )
        except Exception as err:
            logger.error(f"Command synchronization error: {err}", exc_info=True)

    async def on_command_error(self, ctx: Context, error: Exception):
        """
        Handles errors that occur when executing commands with a prefix.
        Overrides the `on_command_error` method from the base class `discord.ext.commands.BotBase`.
        In debug mode, it logs information about a non-existent command.
        """
        if self.config.debug and isinstance(error, CommandNotFound):
            logger.debug(f"Command not found: {ctx.message.content}")
        return None
