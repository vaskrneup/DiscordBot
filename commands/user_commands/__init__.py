from commands.command import (
    BaseCommand,
    auto_parse_sub_commands
)
from .utils import (
    CurrentTime,
    RandomNumber,
    Calc,
    SetTimer
)
from .ai import (
    Search,
    Chat
)


class Main(BaseCommand):
    ACTIVATOR = "bot"
    SUB_COMMANDS = [
        CurrentTime(), RandomNumber(), Calc(), SetTimer(),
        Search(), Chat()
    ]

    @auto_parse_sub_commands
    async def process_request(self, command_text, message_obj) -> str:
        return "Hey, How are you doing !! You can type `main help` to get list of available commands."

    def get_help_text(self):
        return ""
