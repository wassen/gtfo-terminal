#!/usr/bin/env python
# -*- coding:utf-8 -*-

from typing import List

from ..item_property import ItemType
from . import Response


class AddItemType(Response):
    def response_string(self) -> str:
        items_string: List[str] = [
            f"{item.value: >2}: {item.name}" for item in list(ItemType)
        ]
        combined_string: str = "\n".join(items_string)
        with_code_block = f"```\n{combined_string}\n```"
        return f"どのアイテムを保管しますか？数値を入力してください\n{with_code_block}"


class AddItemCount(Response):
    def response_string(self) -> str:
        return "何個入りですか？数値を入力してください"


class AddInAddition(Response):
    def response_string(self) -> str:
        return "アイテム追加中です"


class AddItemEdit(Response):
    def response_string(self) -> str:
        return "へんしゅうちゅう"


AddItemEdit
