#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gtfo_terminal import GTFOTerminal


def __read_token() -> str:
    with open("token") as token_file:
        return token_file.read()

if __name__ == "__main__":
    GTFOTerminal().run(__read_token())

