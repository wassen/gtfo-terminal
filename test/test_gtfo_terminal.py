#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from src.gtfo_terminal import Responder
from src.environment import Env
from src.request import Request


class TestGTFOTerminal(unittest.TestCase):
    def test_hello_on_wakeup(self):
        responder = Responder(env=Env.development)

        self.assertEqual(
            responder.sendRequest(Request.hello).response_string(),
            "bye"
        )


if __name__ == "__main__":
    unittest.main()

