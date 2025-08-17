#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: main.py

Author: WhiteMonsterZeroUltraEnergy
Repository: https://github.com/WhiteMonsterZeroUltraEnergy/PeterGriffin
License: GPL v3

Description:
    The main file you should run.
    At the beginning, start with the --help flag.
"""

from core.discordbot import DiscordBot
from core.config import Config
from utils.logger import set_logger, logger
from utils.tools import parse_args
from pathlib import Path


def main():
    args = parse_args()
    config_path = Path(args.config)
    env_path = Path(args.env)
    log_path = Path(args.logs_path)

    set_logger(log_path, args.debug, args.stream)
    logger.info(f"Logs path: {log_path} - debug: {args.debug} - stream: {args.stream}")

    if not env_path.exists():
        logger.critical(f"Environment file {env_path} not found!")
        exit(1)

    config = Config(
        is_debug=args.debug,
        env_path=env_path,
        config_path=config_path,
    )
    bot = DiscordBot(config=config)

    try:
        bot.run(config.token)
    except Exception as err:
        logger.critical(f"Critical error launching the bot: {err}", exc_info=True)


if __name__ == "__main__":
    main()
