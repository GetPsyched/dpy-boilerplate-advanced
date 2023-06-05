import asyncio
import logging
import os
from typing import Any, Type
from aiohttp import ClientSession

import asyncpg
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

import cogs
from base.context import CustomContext
from utils.logger import ErrorHandler, InfoHandler


class AdvancedBot(commands.Bot):
    """A single-line docstring giving a brief description of the bot"""

    def __init__(
        self,
        *args,
        db_pool: asyncpg.Pool,
        logger: logging.Logger,
        session: ClientSession,
        **kwargs,
    ):
        # It is good practice to manually specify every intent that you will use
        # instead of using discord.Intents.all()
        intents = discord.Intents(
            guilds=True,
            messages=True,
            message_content=True,
            # TODO: Add specific intents as you like
            # Ref: https://discordpy.readthedocs.io/en/stable/api.html#discord.Intents
        )
        super().__init__(
            *args,
            **kwargs,
            command_prefix=self._prefix_callable,
            intents=intents,
        )

        self.pool = db_pool
        self.launch_time = discord.utils.utcnow()
        self.logger = logger
        self.session = session

    @staticmethod
    async def _prefix_callable(bot, message: discord.Message) -> list:
        """Return the bot's prefix for a guild or a DM"""
        await bot.wait_until_ready()

        if os.getenv("DEV") == "1":
            DEFAULT_PREFIX = "!"
        else:
            DEFAULT_PREFIX = "%"

        prefixes = [DEFAULT_PREFIX]

        if message.guild is None:
            return prefixes

        # TODO: Use this if you want saved prefixes
        # saved_prefixes = await bot.pool.fetch(
        #     "SELECT prefix FROM guild_prefix WHERE guild_id = $1",
        #     message.guild.id,
        # )
        # if saved_prefixes:
        #     prefixes = [prefix["prefix"] for prefix in saved_prefixes]

        return prefixes

    async def get_context(
        self,
        origin: discord.Message | discord.Interaction,
        /,
        *,
        cls: Type = None,
    ) -> Any:
        return await super().get_context(origin, cls=cls or CustomContext)

    async def on_ready(self):
        assert self.user is not None
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def setup_hook(self) -> None:
        if os.getenv("DEV") == 1:
            self.logger.addHandler(ErrorHandler(self.loop, self.session))

        results = await asyncio.gather(
            *(self.load_extension(ext) for ext in cogs.INITIAL_EXTENSIONS),
            return_exceptions=True,
        )
        for ext, result in zip(cogs.INITIAL_EXTENSIONS, results):
            if isinstance(result, Exception):
                self.logger.error(f"Failed to load extension `{ext}`: {result}")


async def main():
    dev_bot_token = os.getenv("DEV_BOT_TOKEN")
    assert dev_bot_token is not None

    bot_token = os.getenv("BOT_TOKEN")
    assert bot_token is not None

    logger = logging.getLogger("AdvancedBot")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(InfoHandler())

    discord.utils.setup_logging(level=logging.INFO, root=False)

    pool = asyncpg.create_pool(
        dsn=os.getenv("DSN"), command_timeout=60, max_inactive_connection_lifetime=0
    )
    session = ClientSession()
    bot = AdvancedBot(
        db_pool=pool,
        logger=logger,
        session=session,
    )

    async with session, pool, bot:
        if os.getenv("DEV") == "1":
            await bot.start(dev_bot_token)
        else:
            await bot.start(bot_token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
