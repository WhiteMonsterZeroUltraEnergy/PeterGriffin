"""
File: tools.py

Author: WhiteMonsterZeroUltraEnergy
Repository: https://github.com/WhiteMonsterZeroUltraEnergy/PeterGriffin
License: GPL v3

Description:
    The file responsible for loading the bot configuration from a JSON file and
    parsing the arguments passed at startup.
"""

import argparse
import json
from utils.logger import logger


def parse_args():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [options]",
        description="Opis Petera Griffin.",
        epilog="See https://github.com/WhiteMonsterZeroUltraEnergy",
    )
    parser.add_argument("--debug", "-d", help="Enable debug mode", action="store_true")
    parser.add_argument(
        "--stream", "-s", help="Enable console stream", action="store_true"
    )
    parser.add_argument(
        "--env", help="Path to the .env file (default: .env)", default=".env"
    )
    parser.add_argument(
        "--config",
        help="Path to the config.json file (default: utils/config.json)",
        default="utils/config.json",
    )
    parser.add_argument(
        "--logs-path",
        help="Path to the logs file (default: logs/bot.log)",
        default="logs/bot.log",
    )
    return parser.parse_args()


def load_config_file(path: str = "utils/config.json") -> dict:
    """
    Loads a JSON configuration file containing the bot settings.

    :param path: Path to the configuration file. Default: ‘utils/config.json’.
    :return dict: File contents as a dictionary or empty dictionary in case of error.
    """
    try:
        with open(path) as json_file:
            logger.info(f"Loading config from {path}")
            return json.load(json_file)
    except FileNotFoundError:
        logger.warning(f"Config file not found: {path}")
    except json.JSONDecodeError:
        logger.warning(f"Config file does not contain valid JSON: {path}")
    return {}
