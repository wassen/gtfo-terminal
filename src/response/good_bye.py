#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import Response


class GoodBye(Response):
    should_close: bool = True

    def response_string(self) -> str:
        return "UPLINK DISCONNECTED"
