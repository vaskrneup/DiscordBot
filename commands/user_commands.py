import datetime
import random
import asyncio

from commands.command import (
    BaseCommand,
    auto_parse_sub_commands,
    handle_response_error,
    get_args_only
)


class CurrentTime(BaseCommand):
    async def process_request(self, command_text, message_obj) -> str:
        return f"{datetime.datetime.now():'%Y-%d-%m, %H:%M:%S'}"

    def get_help_text(self):
        return "Get current Date and Time."


class RandomNumber(BaseCommand):
    @handle_response_error(message="Invalid, type help for getting syntax")
    async def process_request(self, command_text, message_obj) -> str:
        numbers = command_text.split(" ")
        return str(random.randint(int(numbers[-2]), int(numbers[-1])))

    def get_help_text(self):
        return f"Get Random number between given range, SYNTAX: `{self.get_activator()} <NUM1> <NUM2>`"


class Calc(BaseCommand):
    @handle_response_error(message="Invalid Expression, Must be valid mathematical Expression.")
    @get_args_only
    async def process_request(self, command_text, message_obj) -> str:
        allowed_chars = "1234567890!@#$%^&*()_+=-|][{}\\;/"
        for c in command_text:
            if c not in allowed_chars:
                return "Please give a valid mathematical expression."

        return str(eval(command_text))

    def get_help_text(self):
        return "Calculate mathematical expressions."


class SetTimer(BaseCommand):
    @handle_response_error(message="Invalid !!")
    @get_args_only
    async def process_request(self, command_text, message_obj) -> str:
        args = command_text.split(" ", 1)
        time, msg = args[0].strip(), " ".join(args[1:])
        await asyncio.sleep(int(time))
        return msg or f"Timer for {time} seconds over !!"

    def get_help_text(self):
        return "sets timer for given seconds."


class Main(BaseCommand):
    SUB_COMMANDS = [CurrentTime(), RandomNumber(), Calc(), SetTimer()]

    @auto_parse_sub_commands
    async def process_request(self, command_text, message_obj) -> str:
        return "Hey, How are you doing !! You can type `main help` to get list of available commands."

    def get_help_text(self):
        return ""
