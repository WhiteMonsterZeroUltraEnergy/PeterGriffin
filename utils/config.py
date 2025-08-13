"""
File: config.py

Author: WhiteMonsterZeroUltraEnergy
Repository: https://github.com/WhiteMonsterZeroUltraEnergy/PeterGriffin
License: GPL v3

Description:
    Configuration class, loading settings from a configuration file and environment variables.
"""

import os
import time
import discord
from dotenv import load_dotenv
from utils.logger import logger
from utils.tools import load_config_file
from pathlib import Path


class Config:
    def __init__(
        self,
        env_path: Path = Path(".env"),
        config_path: Path = Path("utils/config.json"),
        is_debug=True,
    ):
        load_dotenv(env_path)
        self.token: str = os.getenv("DISCORD_TOKEN")
        if not self.token:
            logger.critical("DISCORD_TOKEN not found, check .env file")
            raise ValueError("Brak ustawionego DISCORD_TOKEN w pliku .env")
        self.psql_host: str = os.getenv("PSQL_HOST")
        self.psql_port: int = int(os.getenv("PSQL_PORT"))
        self.psql_db_name: str = os.getenv("PSQL_DB_NAME")
        self.psql_schema: str = os.getenv("PSQL_SCHEMA")
        self.psql_user: str = os.getenv("PSQL_USER")
        self.psql_password: str = os.getenv("PSQL_PASSWORD")
        self.start_timestamp: float = time.time()
        self.debug: bool = is_debug
        self.slash_commands_count: int = 0
        self.cogs_count: int = 0
        # loading config .js file
        self.config_file: dict = load_config_file(config_path.__str__()) or {}
        self.allowed_mentions = discord.AllowedMentions(
            everyone=self.config_file.get("allowed_mentions", {}).get("everyone", True),
            replied_user=self.config_file.get("allowed_mentions", {}).get(
                "replied_user", True
            ),
            users=self.config_file.get("allowed_mentions", {}).get("users", True),
            roles=self.config_file.get("allowed_mentions", {}).get("roles", True),
        )
        self.case_insensitive = self.config_file.get("case_insensitive", True)
        self.owner_id = self.config_file.get("owner_id", None)
        self.owner_ids = self.config_file.get("owner_ids", None)
        self.prefix = self.config_file.get("command_prefix", ";")
        self.status = self.config_file.get("status", None)
        self.strip_after_prefix = self.config_file.get("strip_after_prefix", None)
        self.intents_payload = self.config_file.get("intents_payload", None)
