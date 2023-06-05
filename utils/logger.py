import aiohttp
import asyncio
import logging
import traceback
from os import getenv

import discord


class InfoHandler(logging.Handler):
    def __init__(self):
        super().__init__(logging.INFO)
        self.max_level = logging.INFO
        self.setFormatter(discord.utils._ColourFormatter())

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno <= self.max_level or getenv("DEV") == "1":
            print(self.format(record))


class ErrorHandler(logging.Handler):
    def __init__(self, loop: asyncio.AbstractEventLoop, session: aiohttp.ClientSession):
        super().__init__(logging.WARNING)
        self.loop = loop
        self.webhook = discord.Webhook.from_url(
            getenv("LOG_URL") or "", session=session
        )
        self.setFormatter(discord.utils._ColourFormatter())

        self.colors = {
            "WARNING": discord.Color.orange(),
            "ERROR": discord.Color.red(),
            "CRITICAL": discord.Color.red(),
        }

    def emit(self, record):
        embed = discord.Embed(
            title=record.levelname,
            description=record.msg,
            color=self.colors[record.levelname],
        )

        if record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            tb = "".join(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            )
            embed.add_field(name="Traceback", value=f"```{tb}```", inline=False)

        asyncio.run_coroutine_threadsafe(
            self.webhook.send(
                embed=embed,
                silent=record.levelno < logging.CRITICAL,
            ),
            self.loop,
        )
