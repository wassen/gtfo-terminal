#!/usr/bin/env python
# -*- coding:utf-8 -*-

from typing import Dict, List, Optional

import discord
import sys
from . import state
from .request import Request
from .response import Response
from .response.add import Add
from .response.good_bye import GoodBye
from .environment import Env


store_index: int = 0
store: Dict[int, Dict[str, List[str]]] = {}


def read_help() -> str:
    with open("help") as help_file:
        return help_file.read()


class Command:
    def output(self) -> Optional[int]:
        pass


class ListCommand(Command):
    # output じゃなくてmessage見ればいいのでは
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


class Delete(Command):
    def output(self) -> Optional[int]:
        return self.message

    def __parse(self, elements: List[str]):
        if len(elements) == 0:
            self.message = "indexを指定してください ex) delete 0"
            return

        index = elements[0]

        global store

        deletedItem = store.pop(int(index), None)

        if deletedItem is None:
            self.message = f"indexが{index}なアイテムはないです"
        else:
            self.message = f"以下のアイテムを削除しました{deletedItem}"

    def __init__(self, elements: List[str]):
        self.message = "???"
        self.__parse(elements[1:])


class AddOld(Command):
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
        if len(elements) == 0:
            self.message = "ex) add medi_4 locker_0 zone_1 \n 入力可能文字は, ammo, medi, tool, fog, c-form, melter, mineです"
            return

        storingItem = {
            self.__element_type(element): element.split("_") for element in elements
        }

        global store, store_index
        store[store_index] = storingItem

        self.message = f"index: {store_index}, value{storingItem.__str__()}"
        store_index += 1

    def __init__(self, elements: List[str]):
        self.message = "???"
        self.__parse(elements[1:])


# addの引数ゼロならこっちにする、のほうが良いか
# 1とかのコマンドも含むから、すでにaddコマンドではないんだよなこれ
class AddInteractive(Command):
    def output(self) -> Optional[str]:
        return self.message

    def add_item(self, number: int):
        if number in (item_type.value for item_type in ItemType):
            self.message = "つぎー"
        else:
            self.message = "ないです"

    def interpret_number(self, number: int):
        if state.add_state == state.AddState.item:
            self.add_item(number)
        elif state.add_state == state.AddState.zone:
            pass
        elif state.add_state == state.AddState.container:
            pass
        elif state.add_state == None:
            pass

    def __init__(self, elements: List[str]):
        if elements[0] == "add":
            state.add_state = state.AddState.item
            items_string: List[str] = \
                [f"{item.value: >2}: {item.name}" for item in list(ItemType)]
            combined_string: str = "\n".join(items_string)
            with_code_block = f"```\n{combined_string}\n```"
            self.message = f"どのアイテムを保管しますか？数値を入力してください\n{with_code_block}"
        elif isinstance(number := int(elements[0]), int):
            self.interpret_number(number)
        else:
            pass


class Cancel(Command):
    def output(self) -> Optional[str]:
        return self.message

    def __init__(self):
        state.add_state = None
        self.message = "キャンセルしました"


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
        return AddInteractive(elements)
    elif command == "add":
        return AddOld(elements)
    elif "list".startswith(command):
        return ListCommand(elements)
    elif "delete".startswith(command):
        return Delete(elements)
    else:
        return UnknownCommand()


# Settingのコンストラクタにdevelop or releaseを入れるべきかな
class Setting:
    def __init__(self):
        import yaml

        with open("setting.yaml") as setting_file:
            setting = yaml.safe_load(setting_file)
            self.guild_name: Dict[str, str] = setting["environment"]["guild_name"]
            self.guild_id: Dict[str, int] = setting["environment"]["guild_id"]


class GTFOTerminal(discord.Client):
    async def on_ready(self: discord.Client):
        guild: discord.Guild = next((guild for guild in self.guilds if guild.id == Setting().guild_id[sys.argv[1]]))
        channel: discord.TextChannel = next((channel for channel in guild.channels if channel.name == "gtfo_playing"))
        await channel.send("UPLINK CONNECTED")
        print(f"We have logged in as {self.user}".format())

    async def on_message(self: discord.Client, message: discord.Message):
        if message.author == self.user:
            return

        # 引数なしのときのエラー
        if not message.guild.name == Setting().guild_name[sys.argv[1]]:
            return

        if not message.channel.name == "gtfo_playing":
            return

        request: Request = Request.fromContent(message.content)

        response = Responder().sendRequest(request)

        await message.channel.send(
            response.response_string()
        )

        if response.should_close:
            await self.close()

        # elif state.add_state is not None:
        #     # 重複
        #     # あーもうめちゃくちゃだよ
        #     elements: List[str] = message.content.split(" ")
        #     command = AddInteractive(elements)

        #     output: Optional[str] = command.output()
        #     if command.output() is not None:
        #         await message.channel.send(output)
        # else:
        #     command = parse_command(message.content)

        #     output: Optional[str] = command.output()
        #     if command.output() is not None:
        #         await message.channel.send(output)


class AddResponder():
    pass


class Responder():
    def sendRequest(self, request: Request) -> Response:
        if request == Request.bye:
            return GoodBye()
        elif request == Request.add:
            AddResponder()
            return Add()

