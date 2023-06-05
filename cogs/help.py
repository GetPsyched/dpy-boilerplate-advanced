from discord.ext import commands


class Help(commands.HelpCommand):
    """Help commands"""

    def __init__(self):
        super().__init__(
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.CooldownMapping.from_cooldown(
                    2, 5.0, commands.BucketType.user
                ),
                "aliases": ["commands"],
            }
        )

    async def send(self, **kwargs):
        """A shortcut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    # TODO: Write handler code for each.
    async def send_bot_help(self, mapping):
        """Called when `<prefix>help` is called"""

    async def send_command_help(self, command):
        """Called when `<prefix>help <command>` is called"""

    async def send_help_embed(self, title, description, commands):
        """helper function to add commands to an embed and send it"""

    async def send_group_help(self, group):
        """Called when `<prefix>help <group>` is called"""

    async def send_cog_help(self, cog):
        """Called when `<prefix>help <cog>` is called"""


async def setup(bot):
    bot.help_command = Help()
