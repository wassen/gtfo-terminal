#!/usr/bin/env python
# -*- coding:utf-8 -*-

from typing import Dict, List, Optional

import discord


class Item:
    def __init__(
        self,
        id: int,
        item_type: int,
    ):
        self.id = id
        self.item_type = item_type


store_index: int = 0
store: Dict[int, Dict[str, List[str]]] = {}


def read_token() -> str:
    with open("token") as token_file:
        return token_file.read()


def read_help() -> str:
    with open("help") as help_file:
        return help_file.read()


class Command:
    def output(self) -> Optional[int]:
        pass


class ListCommand(Command):
    def output(self) -> Optional[int]:
        if len(self.message) == 0:
            return "エントリは空です"

        return self.message

    def __parse(self, elements: List[str]):
        formatted_output_line = [f"index: {key}, value: {value.__str__()}" for key, value in store.items()]
        self.message = "\n".join(formatted_output_line)

    def __init__(self, elements: List[str]):
        self.message = "???"
        self.__parse(elements[1:])


class Add(Command):
    def output(self) -> Optional[str]:
        return self.message


    def __element_type(self, element: str) -> Optional[str]:
        # TODO: 別表記をクラスで表現したい
        resources: List[str] = ["ammo", "medi", "tool"]
        consumables: List[str] = ["fog", "c-form", "melter", "mine"]

        if any([element.startswith(item) for item in resources]):
            return "item"
        elif any([element.startswith(item) for item in consumables]):
            return "item"
        elif element.startswith("locker") or element.startswith("box"):
            return "container"
        elif element.startswith("zone"):
            return "zone"
        else:
            return None

    def __parse(self, elements: List[str]):
        if len(elements) == 1:
            self.message = "add help"
            return

        storingItem = {
            self.__element_type(element): element.split("_") for element in elements
        }

        global store, store_index
        store[store_index] = storingItem
        store_index += 1

        self.message = storingItem.__str__()

    def __init__(self, elements: List[str]):
        self.message = "???"
        self.__parse(elements[1:])


class Help(Command):
    def output(self) -> Optional[str]:
        return read_help()


class UnknownCommand:
    def output(self) -> Optional[str]:
        pass


def parse_command(message_content: str) -> Command:
    elements: List[str] = message_content.split(" ")

    command: str = elements[0].lower()

    if "help".startswith(command):
        return Help()
    elif "add".startswith(command):
        return Add(elements)
    elif "list".startswith(command):
        return ListCommand(elements)
    else:
        return UnknownCommand()


class GTFOTerminal(discord.Client):
    async def on_ready(self):
        print(f"We have logged in as {self.user}".format())

    async def on_message(self: discord.Client, message: discord.Message):
        if message.author == self.user:
            return

        if not message.channel.name == "gtfo_playing":
            return

        command = parse_command(message.content)

        output: Optional[str] = command.output()
        if command.output() is not None:
            await message.channel.send(output)


GTFOTerminal().run(read_token())
