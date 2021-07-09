from .command import CommandManager
import discord


class DiscordClient(discord.Client):
    def __init__(self, command_mgr, **options):
        super().__init__(**options)
        self.command_mgr: CommandManager = command_mgr

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author != self.user:
            if resp := await self.command_mgr.parse_command(message.content, message):
                await message.channel.send(resp)
