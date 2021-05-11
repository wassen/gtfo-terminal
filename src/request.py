#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import annotations

from enum import Enum, auto
from typing import Optional


class Request:
    @classmethod
    def fromContent(cls, messageContent: str) -> Optional[Request]:
        byeCommand = [
            "bye",
            "quit",
            "close",
            "disconnect",
        ]
        addCommand = [
            "a",
            "add",
        ]
        listCommand = [
            "l",
            "list",
        ]
        clearCommand = [
            "CLEAR_ALL",
        ]

        if messageContent in byeCommand:
            return CommandRequest.bye
        elif messageContent in addCommand:
            return CommandRequest.add
        elif messageContent in listCommand:
            return CommandRequest.list
        elif messageContent in clearCommand:
            return CommandRequest.clear
        elif isinstance(number := int(messageContent), int):
            return NumberRequest(number)
        else:
            return None


class NumberRequest(Request):
    value: int

    def __init__(self, value: int) -> None:
        self.value = value


class CommandRequest(Request, Enum):
    bye = auto()
    add = auto()
    list = auto()
    clear = auto()
