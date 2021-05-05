#!/usr/bin/env python
# -*- coding:utf-8 -*-

from typing import List

from ..item_property import ItemType
from . import Response
from .choices import AddEditChoice

# class AddItemType(Response):
#     def response_string(self) -> str:
#         items_string: List[str] = [
#             f"{item.value: >2}: {item.itemName}" for item in list(ItemType)
#         ]
#         combined_string: str = "\n".join(items_string)
#         with_code_block = f"```\n{combined_string}\n```"
#         return f"どのアイテムを保管しますか？数値を入力してください\n{with_code_block}"
#
#
# class AddItemCount(Response):
#     def response_string(self) -> str:
#         return "何個入りですか？数値を入力してください"
#
#
# class AddInAddition(Response):
#     def response_string(self) -> str:
#         return "アイテム追加中です"
#
#
# class AddEdit(Response):
#     def response_string(self) -> str:
#         items_string: List[str] = [
#             f"{item.value}: {item.itemName}" for item in list(AddEditChoice)
#         ]
#         combined_string: str = "\n".join(items_string)
#         with_code_block = f"```\n{combined_string}\n```"
#         return f"何を編集しますか？数値を入力してください\n{with_code_block}"
