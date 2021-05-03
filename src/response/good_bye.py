#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import Response


class GoodBye(Response):
    def response_string(self) -> str:
        return "bye"
