import logging
from typing import Any

from discord.ext import commands

from main import AdvancedBot


class BaseCog(commands.Cog):
    """Your base cog. Set vars here which you might use in every cog."""

    def __init__(self, bot: AdvancedBot, *args: Any, **kwargs: Any) -> None:
        self.bot = bot

        super().__init__(*args, **kwargs)

    @property
    def logger(self):
        return logging.getLogger("AdvancedBot")
