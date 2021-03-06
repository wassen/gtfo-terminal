#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
from typing import cast

from src.extension import unwrap
from src.gtfo_terminal import Responder, clear_add_responder
from src.item.item import Item
from src.request import CommandRequest, NumberRequest, Request, RescueRequest
from src.response import Response
from src.response.choices import (AddCompleteResponse,
                                  AddContainerNumberResponse,
                                  AddContainerTypeChoice,
                                  AddContainerTypeResponse, AddEditResponse,
                                  AddInAdditionResponse, AddItemCountResponse,
                                  AddItemTypeChoice, AddItemTypeResponse,
                                  AddZoneNumberResponse)
from src.response.clear import ClearResponse
from src.response.good_bye import GoodByeResponse
from src.response.list import ListResponse
from src.response.rescue import RescueResponse
from src.store.memory_store import clear_store


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


class TestSendClear(unittest.TestCase):
    def test_clear(self) -> None:
        responder = Responder()

        response = responder.send_request(CommandRequest.clear)

        self.assertNotEqual(response, None)
        clear_response = cast(ClearResponse, response)

        # memory_storeに対するテストも作りたいね
        self.assertEqual(
            clear_response.response_string(),
            ClearResponse(clear_response.random_hash).response_string(),
        )

        response = responder.send_request(
            RescueRequest(f"rescue {clear_response.random_hash}")
        )

        self.assertNotEqual(response, None)
        rescue_response = cast(RescueResponse, response)

        # memory_storeに対するテストも作りたいね
        self.assertEqual(
            rescue_response.response_string(),
            RescueResponse(rescue_response.random_hash).response_string(),
        )


class TestSendList(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        clear_store()

    def item1(self) -> Item:
        # builderをItemに作りたい
        item = Item()
        item.item_type = AddItemTypeChoice.ammo
        item.item_count = 1
        item.zone_number = 335
        item.container_type = AddContainerTypeChoice.box
        item.container_number = 1
        item.author_name = "short"
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
            1: self.item1(),
            2: self.item2(),
            3: self.item2(),
            4: self.item2(),
            5: self.item2(),
            6: self.item2(),
            7: self.item2(),
            8: self.item2(),
            9: self.item2(),
            10: self.item2(),
        }

        self.assertEqual(
            ListResponse(items).response_string(),
            "\n".join(
                [
                    "```",
                    "id|   item   |   zone  |container |author|",
                    "------------------------------------------",
                    "01|Ammo:    1|zone: 335| box:    1| short|",
                    "02|L2LP: 1111|zone:   5|lock: 3455|nobody|",
                    "03|L2LP: 1111|zone:   5|lock: 3455|nobody|",
                    "04|L2LP: 1111|zone:   5|lock: 3455|nobody|",
                    "05|L2LP: 1111|zone:   5|lock: 3455|nobody|",
                    "06|L2LP: 1111|zone:   5|lock: 3455|nobody|",
                    "07|L2LP: 1111|zone:   5|lock: 3455|nobody|",
                    "08|L2LP: 1111|zone:   5|lock: 3455|nobody|",
                    "09|L2LP: 1111|zone:   5|lock: 3455|nobody|",
                    "10|L2LP: 1111|zone:   5|lock: 3455|nobody|",
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
    maxDiff = None

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        clear_add_responder()
        clear_store()

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
                    "x|  item |||author|",
                    "-------------------",
                    "1|Ammo: 1|||nobody|",
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
                    "x|  item |  zone |contai|author|",
                    "--------------------------------",
                    "1|Ammo: 1|       |      |nobody|",
                    "2|Ammo: 1|zone: 1|box: 1|nobody|",
                    "```",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
