from commands.command import (
    CommandManager
)
from commands.user_commands import (
    Main
)
from commands.discord import DiscordClient
from utils.config import Config

config = Config()


class CommandMgr(CommandManager):
    COMMANDS = [Main()]


client = DiscordClient(command_mgr=CommandMgr())
client.run(config.get("api_key"))
