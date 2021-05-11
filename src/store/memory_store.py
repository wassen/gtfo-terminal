import hashlib
import random
from typing import Dict, List, NamedTuple, Optional

from ..item.item import Item
from . import Store


# スレッドセーフじゃない、というか複数インスタンス不可なので、インスタンスごとに保存できるか？
# store に名前つけられるようにするか
class MemoryStore(Store):
    class __Column(NamedTuple):
        item: Item
        logical_deleted: bool = False

    __index: int
    __store: Dict[
        int,
        __Column,
    ]

    def add(
        self,
        item: Item,
    ) -> int:
        current_index = self.__index
        self.__index = current_index + 1
        self.__store[current_index] = self.__Column(item)
        return current_index

    def restore(
        self,
        index: int,
    ) -> Optional[Item]:
        targetColumn = self.__store.pop(index, None)

        if (targetColumn := targetColumn) is None:
            return None

        self.__store[index] = self.__Column(
            item=targetColumn.item,
            logical_deleted=False,
        )

        return targetColumn.item

    def drop(
        self,
        index: int,
    ) -> Optional[Item]:
        deletedColumn = self.__store.pop(index, None)

        if (deletedColumn := deletedColumn) is None:
            return None

        self.__store[index] = self.__Column(
            item=deletedColumn.item,
            logical_deleted=True,
        )

        return deletedColumn.item

    def modify(
        self,
        index: int,
        item: Item,
    ) -> None:
        self.__store[index] = self.__Column(
            item=item,
            logical_deleted=False,
        )

    def findAll(
        self,
    ) -> Dict[int, Item]:
        return {key: value.item for key, value in self.__store.items()}

    def __init__(self) -> None:
        self.__index = 1
        self.__store = {}


__past_stores: Dict[str, Store] = {}
__store: Store = MemoryStore()


def __generate_random_hash() -> str:
    # storeのobject_idでもよかったような
    return hashlib.md5(str(random.random()).encode()).hexdigest()


def get_store() -> Store:
    return __store


def clear_store() -> str:
    global __past_stores, __store

    random_hash = __generate_random_hash()
    __past_stores[random_hash] = __store
    __store = MemoryStore()

    return random_hash


def rescue_store(
    key: str,
) -> str:
    global __past_stores, __store

    random_hash = __generate_random_hash()
    __past_stores[random_hash] = __store
    __store = __past_stores[key]

    return random_hash
