#!/usr/bin/env python
# -*- coding:utf-8 -*-

import discord
from typing import Optional

def read_token() -> str:
    with open('token') as token_file:
        return token_file.read()

def read_help() -> str:
    with open('help') as help_file:
        return help_file.read()


class Command:
    def output(self) -> str:
        pass

class Help(Command):
    def output(self) -> str:
        return read_help()

class UnknownCommand:
    def output(self) -> Optional[str]:
        pass

def parse(message_content: str) -> Command:
    elements: list[str] = message_content.split(" ")

    command: str = elements[0].lower()

    if "help".startswith(command):
        return Commands()
    else:
        return UnknownCommand()

class GTFOTerminal(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {self.user}'.format())

    async def on_message(self: discord.Client, message: discord.Message):
        if message.author == self.user:
            return

        if not message.channel.name == 'gtfo_playing':
            return

        command = parse(message.content)

        output: Optional[str] = command.output()
        if command.output() is not None:
            await message.channel.send(output)

GTFOTerminal().run(read_token())

