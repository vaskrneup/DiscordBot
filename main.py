from discord_bot_manager.commands.command import CommandManager
from discord_bot_manager.commands.discord import DiscordClient
from discord_bot_manager.commands.user_commands import Main
from discord_bot_manager.utils.config import Config

config = Config()


class CommandMgr(CommandManager):
    COMMANDS = [Main()]


client = DiscordClient(command_mgr=CommandMgr())
client.run(config.get("api_key"))
