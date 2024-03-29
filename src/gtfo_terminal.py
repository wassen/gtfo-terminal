#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from enum import Enum, auto
from typing import Dict, List, Optional, cast

import discord

from . import state
from .environment import Env
from .item.item import Item
from .request import (CommandRequest, NumberRequest, Request, RescueRequest,
                      SelectRequest)
from .response import Response
from .response.choices import (AddContainerNumberResponse,
                               AddContainerTypeChoice,
                               AddContainerTypeResponse, AddEditChoice,
                               AddEditResponse, AddInAdditionResponse,
                               AddItemCountResponse, AddItemTypeChoice,
                               AddItemTypeResponse, AddResponse, AddState)
from .response.clear import ClearResponse
from .response.good_bye import GoodByeResponse
from .response.list import ListResponse
from .response.rescue import RescueResponse
from .response.select import SelectResponse, SelectState
from .store.memory_store import clear_store, get_store, rescue_store


def read_help() -> str:
    with open("help") as help_file:
        return help_file.read()


class Command:
    def output(self) -> Optional[str]:
        pass


class ListCommand(Command):
    message: str

    # output じゃなくてmessage見ればいいのでは
    def output(self) -> Optional[str]:
        if len(self.message) == 0:
            return "エントリは空です"

        return self.message

    def __parse(self, elements: List[str]) -> None:
        formatted_output_line = [
            f"index: {key}, value: {value.__str__()}"
            for (key, value) in get_store().findAll().items()
        ]
        self.message = "\n".join(formatted_output_line)

    def __init__(self, elements: List[str]):
        self.message = "???"
        self.__parse(elements[1:])


class Delete(Command):
    def output(self) -> Optional[str]:
        return self.message

    def __parse(self, elements: List[str]) -> None:
        if len(elements) == 0:
            self.message = "indexを指定してください ex) delete 0"
            return

        index = elements[0]

        # global store

        # deletedItem = store.pop(int(index), None)

        # if deletedItem is None:
        #     self.message = f"indexが{index}なアイテムはないです"
        # else:
        #     self.message = f"以下のアイテムを削除しました{deletedItem}"

    def __init__(self, elements: List[str]) -> None:
        self.message = "???"
        self.__parse(elements[1:])


# from .item_property import ItemType
# class AddOld(Command):
#     def output(self) -> Optional[str]:
#         return self.message
#
#     def __element_type(self, element: str) -> Optional[str]:
#         # TODO: 別表記をクラスで表現したい
#         resources: List[str] = ["ammo", "medi", "tool"]
#         consumables: List[str] = ["fog", "c-form", "melter", "mine"]
#
#         if any([element.startswith(item) for item in resources]):
#             return "item"
#         elif any([element.startswith(item) for item in consumables]):
#             return "item"
#         elif element.startswith("locker") or element.startswith("box"):
#             return "container"
#         elif element.startswith("zone"):
#             return "zone"
#         else:
#             return None
#
#     def __parse(self, elements: List[str]) -> None:
#         if len(elements) == 0:
#             self.message = "ex) add medi_4 locker_0 zone_1 \n 入力可能文字は, ammo, medi, tool, fog, c-form, melter, mineです"
#             return
#
#         storingItems: Dict[Optional[str], List[str]] = {
#             self.__element_type(element): element.split("_") for element in elements
#         }
#         storingItemsFilterNotNull = {
#             key: value for key, value in storingItems.items() if key is not None
#         }
#
#         global store, store_index
#         store[store_index] = storingItemsFilterNotNull
#
#         self.message = (
#             f"index: {store_index}, value{storingItemsFilterNotNull.__str__()}"
#         )
#         store_index += 1
#
#     def __init__(self, elements: List[str]) -> None:
#         self.message = "???"
#         self.__parse(elements[1:])


# addの引数ゼロならこっちにする、のほうが良いか
# 1とかのコマンドも含むから、すでにaddコマンドではないんだよなこれ
# class AddInteractive(Command):
#     def output(self) -> Optional[str]:
#         return self.message
#
#     def add_item(self, number: int) -> None:
#         if number in (item_type.value for item_type in ItemType):
#             self.message = "つぎー"
#         else:
#             self.message = "ないです"
#
#     def interpret_number(self, number: int) -> None:
#         if state.add_state == state.AddState.item:
#             self.add_item(number)
#         elif state.add_state == state.AddState.zone:
#             pass
#         elif state.add_state == state.AddState.container:
#             pass
#         elif state.add_state is None:
#             pass
#
#     def __init__(self, elements: List[str]) -> None:
#         if elements[0] == "add":
#             state.add_state = state.AddState.item
#             items_string: List[str] = [
#                 f"{item.value: >2}: {item.itemName}" for item in list(ItemType)
#             ]
#             combined_string: str = "\n".join(items_string)
#             with_code_block = f"```\n{combined_string}\n```"
#             self.message = f"どのアイテムを保管しますか？数値を入力してください\n{with_code_block}"
#         elif isinstance(number := int(elements[0]), int):
#             self.interpret_number(number)
#         else:
#             pass


class Cancel(Command):
    def output(self) -> Optional[str]:
        return self.message

    def __init__(self) -> None:
        state.add_state = None
        self.message = "キャンセルしました"


class Help(Command):
    def output(self) -> Optional[str]:
        return read_help()


class UnknownCommand(Command):
    def output(self) -> Optional[str]:
        pass


def parse_command(message_content: str) -> Command:
    elements: List[str] = message_content.split(" ")

    command: str = elements[0].lower()

    if "help".startswith(command):
        return Help()
    elif "add".startswith(command):
        raise Exception()
        # return AddInteractive(elements)
    elif command == "add":
        raise Exception()
        # return AddOld(elements)
    elif "list".startswith(command):
        return ListCommand(elements)
    elif "delete".startswith(command):
        return Delete(elements)
    else:
        return UnknownCommand()


# Settingのコンストラクタにdevelop or releaseを入れるべきかな
class Setting:
    def __init__(self) -> None:
        import yaml

        with open("setting.yaml") as setting_file:
            setting = yaml.safe_load(setting_file)
            self.guild_name: Dict[str, str] = setting["environment"]["guild_name"]
            self.guild_id: Dict[str, int] = setting["environment"]["guild_id"]


class GTFOTerminal(discord.Client):
    async def on_ready(self: discord.Client) -> None:
        guild: discord.Guild = next(
            (
                guild
                for guild in self.guilds
                if guild.id == Setting().guild_id[sys.argv[1]]
            )
        )
        channel = next(
            (
                channel
                for channel in guild.channels
                if channel.name == "gtfo_playing"
                and type(channel) == discord.TextChannel
            )
        )
        textChannel = cast(discord.TextChannel, channel)

        await textChannel.send("UPLINK CONNECTED")
        print(f"We have logged in as {self.user}".format())

    async def on_message(self: discord.Client, message: discord.Message) -> None:
        if message.author == self.user:
            return

        if (guild := message.guild) is None:
            return

        # 引数なしのときのエラー
        if not guild.name == Setting().guild_name[sys.argv[1]]:
            return

        if type(channel := message.channel) != discord.TextChannel:
            return
        textChannel = cast(discord.TextChannel, channel)

        if not textChannel.name == "gtfo_playing":
            return

        request = Request.fromContent(message.content)
        if request is None:
            return

        response = Responder().send_request(
            request,
            member_name=message.author.name,
        )

        if response is None:
            return

        await message.channel.send(response.response_string())

        # reponseをobjectにしたい唯一の理由
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


class SelectResponder:
    current_state: SelectState
    item: Item
    index: int

    def firstResponse(self) -> SelectResponse:
        return SelectEditResponse()

    def sendNumber(self, number: int) -> Optional[AddResponse]:
        if self.current_state == AddState.item_type:
            self.item.item_type = AddItemTypeChoice(number)
            self.current_state = AddState.item_count
            return AddItemCountResponse()
        elif self.current_state == AddState.item_count:
            self.item.item_count = number
            self.current_state = AddState.edit
            return AddEditResponse()
        elif self.current_state == AddState.edit:
            if (next_state := AddEditChoice(number).next_state()) is None:
                return "ぬぬ"
            else:
                self.current_state = next_state
                return next_state.response()
        elif self.current_state == AddState.zone_number:
            self.item.zone_number = number
            self.current_state = AddState.edit
            return AddEditResponse()
        elif self.current_state == AddState.container_type:
            self.item.container_type = AddContainerTypeChoice(number)
            self.current_state = AddState.container_number
            return AddContainerNumberResponse()
        elif self.current_state == AddState.container_number:
            self.item.container_number = number
            self.current_state = AddState.edit
            return AddEditResponse()
        else:
            return None

    def __init__(self, index: int) -> None:
        self.curernt_state = SelectState.edit
        self.item = Item()
        self.index = index


class AddResponder:
    current_state: AddState = AddState.item_type
    item: Item

    def firstResponse(self) -> AddResponse:
        return AddItemTypeResponse()

    def sendNumber(self, number: int) -> Optional[AddResponse]:
        if self.current_state == AddState.item_type:
            self.item.item_type = AddItemTypeChoice(number)
            self.current_state = AddState.item_count
            return AddItemCountResponse()
        elif self.current_state == AddState.item_count:
            self.item.item_count = number
            self.current_state = AddState.edit
            return AddEditResponse()
        elif self.current_state == AddState.edit:
            if (next_state := AddEditChoice(number).next_state()) is None:
                return "ぬぬ"
            else:
                self.current_state = next_state
                return next_state.response()
        elif self.current_state == AddState.zone_number:
            self.item.zone_number = number
            self.current_state = AddState.edit
            return AddEditResponse()
        elif self.current_state == AddState.container_type:
            self.item.container_type = AddContainerTypeChoice(number)
            self.current_state = AddState.container_number
            return AddContainerNumberResponse()
        elif self.current_state == AddState.container_number:
            self.item.container_number = number
            self.current_state = AddState.edit
            return AddEditResponse()
        else:
            return None

    def __init__(self) -> None:
        self.curernt_state = AddState.item_type
        self.item = Item()


add_responder: Optional[AddResponder] = None
select_responder: Optional[SelectResponder] = None


# ストアは別モジュールにしたい
def clear_add_responder() -> None:
    global add_responder
    add_responder = None


# ResponderがStoreにアクセスするのはどうなんだ？と思いつつも、ユーザーのRequestを解釈するのがResponderで、
# つまりItemを作れるのはResponderだけ
# Responderが解釈してActionを作り、Actionを返し、ActionにItemを内包させる、とかだろうか
class Responder:
    def send_request(
        self, request: Request, member_name: str = "nobody"
    ) -> Optional[Response]:
        global add_responder, select_responder

        if request == CommandRequest.bye:
            return GoodByeResponse()
        elif request == CommandRequest.add:
            if add_responder is None:
                add_responder = AddResponder()
                # firstResponseとAddInAdditionで一貫性がない
                return add_responder.firstResponse()
            else:
                return AddInAdditionResponse()
        elif request == CommandRequest.list:
            return ListResponse(get_store().findAll())
        elif request == CommandRequest.clear:
            random_hash = clear_store()
            return ClearResponse(random_hash)
        elif type(request) is SelectRequest:
            selectRequest = cast(SelectRequest, request)

            if select_responder is None:
                select_responder = SelectResponder(request.index)
                return select_responder.firstResponse()
            else:
                return SelectInSelectionResponse()

            previous_random_hash = rescue_store(selectRequest.random_hash)
            return SelectResponse(previous_random_hash)
        elif type(request) is RescueRequest:
            rescueRequest = cast(RescueRequest, request)

            previous_random_hash = rescue_store(rescueRequest.random_hash)
            return RescueResponse(previous_random_hash)
        elif type(request) is NumberRequest:
            numberRequest = cast(NumberRequest, request)
            if (ar := add_responder) is not None:
                if (response := ar.sendNumber(numberRequest.value)) is not None:
                    # ネスト深すぎ
                    if response.complete:
                        item = ar.item
                        item.author_name = member_name
                        get_store().add(item)
                        add_responder = None

                    return response
            elif ((sr := select_responder) is not None) and (
                response := sr.send_number(numberRequest.value)
            ) is not None:
                if response.complete:
                    select_responder = None

                if response.modify:
                    item = sr.item
                    index = sr.index
                    item.author_name = member_name
                    get_store().modify(index, item)
                elif response.delete:
                    index = sr.index
                    get_store().delete(index)
                else:
                    raise Exception()

                return response
            else:
                return None

        else:
            raise Exception()
