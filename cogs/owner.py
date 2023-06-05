from typing import Literal, Optional

import discord
from discord.ext import commands

from base.cog import BaseCog
from main import AdvancedBot


class Owner(BaseCog):
    """Bot owner commands"""

    async def cog_check(self, ctx: commands.Context[AdvancedBot]) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(hidden=True)
    async def load(self, ctx: commands.Context[AdvancedBot], *, module: str):
        """Loads a module."""
        try:
            await self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send("\N{OK HAND SIGN}")

    @commands.command(hidden=True)
    async def unload(self, ctx: commands.Context[AdvancedBot], *, module: str):
        """Unloads a module."""
        try:
            await self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send("\N{OK HAND SIGN}")

    @commands.group(name="reload", hidden=True, invoke_without_command=True)
    async def _reload(self, ctx: commands.Context[AdvancedBot], *, module: str):
        """Reloads a module."""
        try:
            await self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send("\N{OK HAND SIGN}")

    @commands.command()
    @commands.guild_only()
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot):
    await bot.add_cog(Owner(bot))
