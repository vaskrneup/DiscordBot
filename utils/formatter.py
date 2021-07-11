def get_help_text_from_list(commands):
    if not commands:
        return ""

    max_command_length = max(
        [*[len(str(command)) for command in commands], len('COMMANDS')]
    ) + len("[syntax]") + 2
    max_command_help_text_length = max(
        (len(command.get_help_text()) for command in commands)
    )

    out = ""
    out += (
            f"`{'commands':<{max_command_length}}| help" +
            " " * (max_command_help_text_length - 4) +
            "\n"
    )
    out += (
            "-" * (max_command_help_text_length + max_command_length + 2) +
            "\n"
    )

    for command in commands:
        out += (
                f"{str(command):<{max_command_length}}| {command.get_help_text()}" +
                " " * (max_command_help_text_length - len(command.get_help_text())) +
                "\n"
        )
        out += (
                f"{str(command) + '[syntax]':<{max_command_length}}| {command.get_command_syntax()}" +
                " " * (max_command_help_text_length - len(command.get_command_syntax())) +
                "\n"
        )

    out += "`"
    return out
