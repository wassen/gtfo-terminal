from typing import Dict, List, NamedTuple, Optional

from ..item.item import Item
from . import Store


class __Column(NamedTuple):
    item: Item
    logical_deleted: bool = False


__index: int = 0
__store: Dict[
    int,
    __Column,
]


# スレッドセーフじゃない、というか複数インスタンス不可なので、インスタンスごとに保存できるか？
# store に名前つけられるようにするか
class MemoryStore(Store):
    def clear(
        self,
    ) -> None:
        global __index, __store

        __index = 0
        __store = {}

    def add(
        self,
        item: Item,
    ) -> int:
        global __index, __store

        current_index = __index
        __index = current_index + 1
        __store[current_index] = __Column(item)
        return current_index

    def restore(
        self,
        index: int,
    ) -> Optional[Item]:
        global __store

        targetColumn = __store.pop(index, None)

        if (targetColumn := targetColumn) is None:
            return None

        __store[index] = __Column(
            item=targetColumn.item,
            logical_deleted=False,
        )

        return targetColumn.item

    def drop(
        self,
        index: int,
    ) -> Optional[Item]:
        global __store

        deletedColumn = __store.pop(index, None)

        if (deletedColumn := deletedColumn) is None:
            return None

        __store[index] = __Column(
            item=deletedColumn.item,
            logical_deleted=True,
        )

        return deletedColumn.item

    def modify(
        self,
        index: int,
        item: Item,
    ) -> None:
        global __store

        __store[index] = __Column(
            item=item,
            logical_deleted=False,
        )

    def findAll(
        self,
    ) -> Dict[int, Item]:
        return {}
