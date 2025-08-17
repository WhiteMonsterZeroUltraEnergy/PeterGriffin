#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .fun import Fun

async def setup(bot):
    await bot.add_cog(Fun(bot))
