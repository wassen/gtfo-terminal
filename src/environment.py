#!/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum, auto


class Env(Enum):
    development = auto()
    release = auto()

    @classmethod
    def fromName(cls, name: str) -> "Env":
        # TODO: throwable
        return next(item for item in Env if item.name == name)
