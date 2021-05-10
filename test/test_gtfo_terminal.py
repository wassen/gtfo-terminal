#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from typing import cast

from src.extension import unwrap
from src.gtfo_terminal import Responder, clear_add_responder
from src.item.item import Item
from src.request import CommandRequest, NumberRequest, Request
from src.response import Response
from src.response.choices import (AddCompleteResponse,
                                  AddContainerNumberResponse,
                                  AddContainerTypeChoice,
                                  AddContainerTypeResponse, AddEditResponse,
                                  AddInAdditionResponse, AddItemCountResponse,
                                  AddItemTypeChoice, AddItemTypeResponse,
                                  AddZoneNumberResponse)
from src.response.good_bye import GoodByeResponse
from src.response.list import ListResponse
from src.store.memory_store import MemoryStore


class TestSendBye(unittest.TestCase):
    def test_bye(self) -> None:
        responder = Responder()

        response = responder.send_request(CommandRequest.bye)
        self.assertNotEqual(response, None)
        response = cast(Response, response)

        self.assertEqual(
            response.response_string(),
            GoodByeResponse().response_string(),
        )


class TestSendList(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        MemoryStore().clear()

    def item1(self) -> Item:
        # builderをItemに作りたい
        item = Item()
        item.item_type = AddItemTypeChoice.ammo
        item.item_count = 1
        item.zone_number = 335
        item.container_type = AddContainerTypeChoice.box
        item.container_number = 1
        return item

    def item2(self) -> Item:
        # builderをItemに作りたい
        item = Item()
        item.item_type = AddItemTypeChoice.l2_lp_syringe
        item.item_count = 1111
        item.zone_number = 5
        item.container_type = AddContainerTypeChoice.locker
        item.container_number = 3455
        return item

    def test_format(self) -> None:
        items = {
            0: self.item1(),
            1: self.item2(),
        }

        self.assertEqual(
            ListResponse(items).response_string(),
            "\n".join(
                [
                    "```",
                    "x|          |         |          |",
                    "0|Ammo:    1|zone: 335| box:    1|",
                    "1|L2LP: 1111|zone:   5|lock: 3455|",
                    "```",
                ]
            ),
        )

    def test_short_name_length(self) -> None:
        self.assertTrue(
            all([len(item.short_name) == 4 for item in AddItemTypeChoice]),
        )


class TestSendOnlyList(unittest.TestCase):
    def test_only_list(self) -> None:
        responder = Responder()

        response = unwrap(responder.send_request(CommandRequest.list))

        # 何を追加しますか？
        self.assertEqual(
            response.response_string(),
            "No items",  # 重複定義
        )


class TestSendAdd(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        clear_add_responder()
        MemoryStore().clear()

    def test_add1(self) -> None:
        responder = Responder()

        response = unwrap(responder.send_request(CommandRequest.add))

        # 何を追加しますか？
        self.assertEqual(
            response.response_string(),
            AddItemTypeResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        # アイテムの数は？
        self.assertEqual(
            response.response_string(),
            AddItemCountResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        # 何編集する？
        self.assertEqual(
            response.response_string(),
            AddEditResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(0)))

        # 完了しました
        self.assertEqual(
            response.response_string(),
            AddCompleteResponse().response_string(),
        )

        response = unwrap(responder.send_request(CommandRequest.list))

        self.assertEqual(
            response.response_string(),
            "\n".join(
                [
                    "```",
                    "x|       |||",
                    "0|Ammo: 1|||",
                    "```",
                ]
            ),
        )

        response = unwrap(responder.send_request(CommandRequest.add))

        # 何を追加しますか？
        self.assertEqual(
            response.response_string(),
            AddItemTypeResponse().response_string(),
        )

        response = unwrap(responder.send_request(CommandRequest.add))

        # 追加中にaddしないで
        self.assertEqual(
            response.response_string(),
            AddInAdditionResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        # アイテムの数は？
        self.assertEqual(
            response.response_string(),
            AddItemCountResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        # 何編集する？
        self.assertEqual(
            response.response_string(),
            AddEditResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        # ゾーン番号は？
        self.assertEqual(
            response.response_string(),
            AddZoneNumberResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        # 何編集する？
        self.assertEqual(
            response.response_string(),
            AddEditResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(2)))

        # 入れ物タイプは？
        self.assertEqual(
            response.response_string(),
            AddContainerTypeResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        # 入れ物番号は？
        self.assertEqual(
            response.response_string(),
            AddContainerNumberResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(1)))

        # 何編集する？
        self.assertEqual(
            response.response_string(),
            AddEditResponse().response_string(),
        )

        response = unwrap(responder.send_request(NumberRequest(0)))

        # 完了しました
        self.assertEqual(
            response.response_string(),
            AddCompleteResponse().response_string(),
        )

        response = unwrap(responder.send_request(CommandRequest.list))

        self.assertEqual(
            response.response_string(),
            "\n".join(
                [
                    "```",
                    "x|       |       |      |",
                    "0|Ammo: 1|       |      |",
                    "1|Ammo: 1|zone: 1|box: 1|",
                    "```",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
