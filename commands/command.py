class CommandManager:
    COMMANDS = []

    def __init__(self):
        self.activators: dict = {command.get_activator(): command for command in self.COMMANDS}

    async def parse_command(self, command, message_obj=None):
        main_command = command.split(" ", 1)[0].strip()

        if main_command in self.activators:
            command_executor = self.activators[main_command]
            return await command_executor.process_request(command, message_obj)
        elif command == "help":
            return self.create_help_text_from_list()

    def create_help_text_from_list(self):
        if not self.COMMANDS:
            return ""

        max_command_length = max([*[len(str(command)) for command in self.COMMANDS], len('COMMANDS')])
        out = ""

        out += f"`{'COMMANDS':<{max_command_length}}  | HELP\n"
        for command in self.COMMANDS:
            out += f"{str(command):<{max_command_length}}  |  {command.get_help_text()}\n"

        out += "`"
        return out


class BaseCommand:
    SUB_COMMANDS = []
    ACTIVATOR: str = None

    def __init__(self):
        self.__activator = self.ACTIVATOR if self.ACTIVATOR is not None else str(self.__class__.__name__.lower())
        self.activators: dict = {command.get_activator(): command for command in self.SUB_COMMANDS}

    def get_activator(self):
        return self.__activator

    async def process_request(self, command_text, message_obj) -> str:
        raise NotImplementedError

    def get_help_text(self):
        raise NotImplementedError

    async def parse_command(self, command, message_obj):
        main_command = command.split(" ", 1)[0].strip()

        if main_command in self.activators:
            command_executor = self.activators[main_command]
            if command.endswith(" help"):
                _help = command_executor.get_help_text()
                if help_for_sub_commands := command_executor.create_help_text_from_list():
                    _help += "\n"
                    _help += "-" * int(len(_help) * 1.3)
                    _help += f"\n{help_for_sub_commands}"
                return _help

            return await command_executor.process_request(command, message_obj)
        elif command == "help":
            return self.create_help_text_from_list()

    def create_help_text_from_list(self):
        if self.SUB_COMMANDS:
            max_command_length = max([*[len(str(command)) for command in self.SUB_COMMANDS], len("COMMANDS")])
            out = ""

            out += f"`{'COMMANDS':<{max_command_length}}  |  HELP\n"
            for command in self.SUB_COMMANDS:
                out += f"{str(command):<{max_command_length}}  |  {command.get_help_text()}\n"
            out += "`"

            return out

    def __str__(self):
        return self.get_activator()


def auto_parse_sub_commands(func):
    async def wrapper(self, command, *args, **kwargs):
        new_command = command.replace(self.get_activator(), "").strip()
        if sub_command_data := await self.parse_command(new_command, *args, **kwargs):
            return sub_command_data
        else:
            return await func(self, command, *args, **kwargs)

    return wrapper


def handle_response_error(message="Something wrong happened !"):
    def inner(func):
        async def wrapper(self, command_text, *args, **kwargs):
            try:
                return await func(self, command_text, *args, **kwargs)
            except Exception as _:  # NOQA
                return message

        return wrapper

    return inner


def get_args_only(func):
    async def wrapper(self, command_text, *args, **kwargs):
        return await func(self, command_text.replace(self.get_activator(), "").strip(), *args, **kwargs)

    return wrapper
