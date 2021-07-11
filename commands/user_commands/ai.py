import re

from commands.command import (
    BaseCommand,
    auto_parse_sub_commands,
    get_args_only
)
from utils.search import search


class Search(BaseCommand):
    @get_args_only
    async def process_request(self, command_text, message_obj) -> str:
        return search(command_text)

    def get_help_text(self):
        return "Searches the internet for your query."


class Chat(BaseCommand):
    ACTIVATOR = "ai"

    @auto_parse_sub_commands
    @get_args_only
    async def process_request(self, command_text, message_obj) -> str:
        known_queries = re.compile("(who is|what is|how to)")

        if known_queries.match(command_text):
            return search(command_text)
        else:
            return "WHAT ??"

    def get_help_text(self):
        return "Tries to give response to your queries."
