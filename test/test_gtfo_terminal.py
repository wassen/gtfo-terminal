#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest

from src.environment import Env
from src.gtfo_terminal import Responder
from src.request import Request
from src.response.add import Add
from src.response.good_bye import GoodBye


class TestSendBye(unittest.TestCase):
    def test_bye(self):
        responder = Responder()

        self.assertEqual(
            responder.sendRequest(Request.bye).response_string(),
            GoodBye().response_string(),
        )


class TestSendAdd(unittest.TestCase):
    def test_add_start(self):
        responder = Responder()

        self.assertEqual(
            responder.sendRequest(Request.add).response_string(),
            Add().response_string(),
        )


if __name__ == "__main__":
    unittest.main()
