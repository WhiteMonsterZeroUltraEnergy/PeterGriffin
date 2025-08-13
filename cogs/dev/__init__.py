#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.logger import logger
from .dev import Dev


async def setup(bot):
    await bot.add_cog(Dev(bot))


async def teardown(bot):
    logger.warning("cogs.dev: Unloaded!")
