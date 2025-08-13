# Peter Griffin

![image](https://cdn.discordapp.com/attachments/1387294678931734640/1405055696063565834/Piotr.jpg?ex=689d6f96&is=689c1e16&hm=572677b05b013f8fcb15b1c60bc4e603ba09f9d560fdf8ed56ae2dd3158005b0&)

**Piotr Gryf** is a man of many talents, multidimensional, unconventional, unattainable for the beings of this world, modest but at the same time fond of showing his golden pearl claw, a mine of ideas, a monumental figure, an inspired leader, a polyglot and philosopher, a Nobel laureate, a scholar in speech and writing, the patriarch of the nation, Lech Wałęsa.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub License](https://img.shields.io/github/license/WhiteMonsterZeroUltraEnergy/PeterGriffin)
[![Static Badge](https://img.shields.io/badge/discord.py-5865F2)](https://github.com/Rapptz/discord.py)


## Table of contents

- [Requirements](#Requirements)
- [Installation](#Installation)
- [Configuration](#Configuration)
- [License](#License)
- [FAQ](#FAQ)

## Requirements

Before launching the bot, make sure you have:

- Python 3.8 or higher
- Fill in the .env file
- Installed dependencies `requirements.txt` (see below)
- Bot token generated on [Discord Developer Portal](https://discord.com/developers/applications)
- Select the options `applications.commands` and `bot` in the OAuth2 URL Generator
- Check configuration file `utils/config.json`

## Installation

### 1. Clone the repository

```
git clone https://github.com/WhiteMonsterZeroUltraEnergy/PeterGriffin.git
```

```
cd PeterGriffin/
```

### 2. Create a virtual environment [venv](https://docs.python.org/3/library/venv.html)

```
python3 -m venv venv
```

When you want to enter `venv`
```
source venv/bin/activate
```

When you want to leave
```
deactivate
```

### 3. Install the required libraries

```
pip install -r requirements.txt
```

### 4. Fill in the `.env` file

If the `.env` file does not exist, create it:

```
touch .env
```

Then enter your token and the rest of the variables (for PostgreSQL):

```
DISCORD_TOKEN=YOUR_BOT_TOKEN
PSQL_HOST="192.168.x.x"
PSQL_PORT=5432
PSQL_DB_NAME="peter_griffin_db"
PSQL_SCHEMA="dev"
PSQL_USER="myuser"
PSQL_PASSWORD="mypassword"
```

### 5. Launch the bot

#### Check out `--help` as well.

```
python3 main.py --help
```

#### Running the bot in debug mode (check `logs/bot.log`)

```
python3 main.py --debug
```

#### Running the bot in the background

```
python3 main.py >/dev/null 2>&1 &
```

## Configuration

**WiP**

See `config.md`

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3). 

See the LICENSE file for details.

## FAQ

- **ModuleNotFoundError: No module named 'discord'** → Check if you have installed the dependencies (`pip install -r requirements.txt`).

- **The bot does not respond to commands** → Check if it has the appropriate permissions on the server, or check [Intents](https://discord.com/developers/docs/developer-tools/community-resources#intent-calculators).

- **The bot has no new features, but there was no error when loading `cogs`.** → Restart the Discord application (client) or press `CTRL+R`.

- **After registering the bot on the server, it may take a few minutes before the (`/`) slash commands become available on the server.** Sometimes it may take a while for the bot to sync.
