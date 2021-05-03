#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import annotations
from enum import auto, Enum


class Request(Enum):
    bye = auto()

    byeCommand = ["bye", "quit", "close", "disconnect"]

    @classmethod
    def fromContent(cls, messageContent: str) -> Request:
        if messageContent in cls.byeCommand:
            return Request.bye

