#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import annotations

from enum import Enum, auto
from typing import Optional


class Request(Enum):
    bye = auto()
    add = auto()

    @classmethod
    def fromContent(cls, messageContent: str) -> Optional[Request]:
        byeCommand = ["bye", "quit", "close", "disconnect"]
        addCommand = ["add"]

        if messageContent in byeCommand:
            return Request.bye
        elif messageContent in addCommand:
            return Request.add
        else:
            return None
