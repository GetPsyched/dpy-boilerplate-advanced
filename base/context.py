from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext.commands import Context

if TYPE_CHECKING:
    from main import AdvancedBot


class CustomContext(Context['AdvancedBot']):
    """Your custom context. Override any context method here."""
