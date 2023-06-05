import discord
from discord import app_commands
from discord.ext import commands

from base.cog import BaseCog
from base.context import CustomContext
from main import AdvancedBot


class Errors(BaseCog):
    """Global Error Handler"""

    def __init__(self, bot: AdvancedBot):
        super().__init__(bot)
        print(0)
        self.bot.tree.on_error = self.on_app_command_error

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx: CustomContext,
        error: commands.CommandError,
    ):
        """Handle prefix command errors here."""
        print(1)
        self.logger.exception(error)
        raise error

    async def on_app_command_error(
        self,
        interaction: discord.Interaction[AdvancedBot],
        error: app_commands.AppCommandError,
    ):
        """Handle slash command errors here."""
        caught: bool = False
        error_text: str = error.__class__.__name__

        if not caught:
            self.logger.exception(error)

        if interaction.response.is_done():
            await interaction.followup.send(error_text, ephemeral=True)
        else:
            await interaction.response.send_message(error_text, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Errors(bot))
