"""
File: database.py

Author: WhiteMonsterZeroUltraEnergy
Repository: https://github.com/WhiteMonsterZeroUltraEnergy/PeterGriffin
License: GPL v3

Description:
    A class that handles connections to the Postgresql database,
    offering methods for executing queries and retrieving results.
"""

import asyncpg
from utils.logger import logger


class Database:
    """Class handling connection to Postgresql database."""

    def __init__(
        self, host: str, port: int, database: str, schema: str, user: str, password: str
    ):
        self.host = host
        self.port = port
        self.database = database
        self.schema = schema
        self.user = user
        self.password = password
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                command_timeout=60,
                init=self._init_connection
            )
            logger.info(f"Postgresql: Connected to {self.host}:{self.port}")

    async def _init_connection(self, conn):
        await conn.execute(f"SET search_path TO {self.schema}")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None
            logger.critical(f"Postgresql: Disconnected from {self.host}:{self.port}")

    async def execute(self, query: str, *args) -> str | None:
        """
        Execute an SQL command (or commands).

        :param query: SQL command to be executed.
        :param args: Arguments to parameterize the SQL command.
        :return: Status string of the last SQL command executed,
        or None if not connected.
        """
        if not self.pool:
            logger.warning(f"Postgresql: Not connected to {self.host}:{self.port}")
            return None
        async with self.pool.acquire() as conn:
            await conn.execute(f"SET search_path TO {self.schema}")
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> list[asyncpg.Record] | None:
        """
        Run a query and return the results as a list of :class:`Record`.

        :param query: SQL query to be executed.
        :param args: Arguments to parameterize the SQL query.
        :return: List of `asyncpg.Record` instances resulting from the query,
        or None if not connected.
        """
        if not self.pool:
            logger.warning(f"Postgresql: Not connected to {self.host}:{self.port}")
            return None
        async with self.pool.acquire() as conn:
            await conn.execute(f"SET search_path TO {self.schema}")
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> asyncpg.Record | None:
        """
        Run a query and return the first row.

        :param query: SQL query to be executed.
        :param args: Arguments to parameterize the SQL query.
        :return: A single `asyncpg.Record` instance representing the first row,
        or None if no rows returned or not connected.
        """
        if not self.pool:
            logger.warning(f"Postgresql: Not connected to {self.host}:{self.port}")
            return None
        async with self.pool.acquire() as conn:
            await conn.execute(f"SET search_path TO {self.schema}")
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args):
        """
        Run a query and return a value in the first row.

        :param query: SQL query to be executed.
        :param args: Arguments to parameterize the SQL query.
        :return: A scalar value from the first column of the first row,
        or None if no rows returned or not connected.
        """
        if not self.pool:
            logger.warning(f"Postgresql: Not connected to {self.host}:{self.port}")
            return None
        async with self.pool.acquire() as conn:
            await conn.execute(f"SET search_path TO {self.schema}")
            return await conn.fetchval(query, *args)
