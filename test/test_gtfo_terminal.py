#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from typing import cast

from src.extension import unwrap
from src.gtfo_terminal import Responder, clear_add_responder
from src.request import CommandRequest, NumberRequest, Request
from src.response.choices import (AddEditResponse, AddInAdditionResponse,
                                  AddItemCountResponse, AddItemTypeResponse)
from src.response.good_bye import GoodByeResponse


class TestSendBye(unittest.TestCase):
    def test_bye(self) -> None:
        responder = Responder()

        response = responder.send_request(CommandRequest.bye)
        self.assertNotEqual(response, None)
        response = cast(str, response)

        self.assertEqual(
            response,
            GoodByeResponse().response_string(),
        )


class TestSendAdd(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        clear_add_responder()

    def test_add(self) -> None:
        responder = Responder()

        response = unwrap(responder.send_request(CommandRequest.add))

        self.assertEqual(
            response,
            AddItemTypeResponse().response_string(),
        )

        response = unwrap(responder.send_request(CommandRequest.add))

        self.assertEqual(
            response,
            AddInAdditionResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        self.assertEqual(response, AddItemCountResponse().response_string())

        response = unwrap(responder.send_request(NumberRequest(1)))

        self.assertEqual(response, AddEditResponse().response_string())

        response = unwrap(responder.send_request(NumberRequest(1)))

        self.assertEqual(response, AddZoneNumberResponse().response_string())


if __name__ == "__main__":
    unittest.main()
