"""
File: logger.py

Author: WhiteMonsterZeroUltraEnergy
Repository: https://github.com/WhiteMonsterZeroUltraEnergy/PeterGriffin
License: GPL v3

Description:
    Configures the logger with the ability to set the log level,
    write to a file, and stream logs to the console.
"""

import logging
from pathlib import Path

logger = logging.getLogger("bot")
discord_logger = logging.getLogger("discord.client")
http_logger = logging.getLogger("discord.http")
app_commands = logging.getLogger("discord.app_commands.tree")


def set_logger(
    log_path: Path = Path("logs/bot.log"), debug: bool = False, stream: bool = False
) -> None:
    """
    Configures the logger for the application and the specified additional loggers.

    :param log_path: Path to the log file.
    :param debug: If True, sets the DEBUG level, otherwise INFO.
    :param stream: If True, it also logs to the console.
    :return: None
    """
    if logger.hasHandlers():
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )

    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    discord_logger.setLevel(level)
    http_logger.setLevel(level)
    app_commands.setLevel(level)

    file_handler = logging.FileHandler(filename=log_path, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    discord_logger.addHandler(file_handler)
    http_logger.addHandler(file_handler)
    app_commands.addHandler(file_handler)

    if stream:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        discord_logger.addHandler(console_handler)
        http_logger.addHandler(console_handler)
        app_commands.addHandler(console_handler)
