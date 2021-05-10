from typing import Dict, List, NamedTuple, Optional

from ..item.item import Item
from . import Store


class _Column(NamedTuple):
    item: Item
    logical_deleted: bool = False


_index: int = 1
_store: Dict[
    int,
    _Column,
] = {}

# スレッドセーフじゃない、というか複数インスタンス不可なので、インスタンスごとに保存できるか？
# store に名前つけられるようにするか
class MemoryStore(Store):
    def clear(
        self,
    ) -> None:
        global _index, _store

        _index = 1
        _store = {}

    def add(
        self,
        item: Item,
    ) -> int:
        global _index, _store

        current_index = _index
        _index = current_index + 1
        _store[current_index] = _Column(item)
        return current_index

    def restore(
        self,
        index: int,
    ) -> Optional[Item]:
        global _store

        targetColumn = _store.pop(index, None)

        if (targetColumn := targetColumn) is None:
            return None

        _store[index] = _Column(
            item=targetColumn.item,
            logical_deleted=False,
        )

        return targetColumn.item

    def drop(
        self,
        index: int,
    ) -> Optional[Item]:
        global _store

        deletedColumn = _store.pop(index, None)

        if (deletedColumn := deletedColumn) is None:
            return None

        _store[index] = _Column(
            item=deletedColumn.item,
            logical_deleted=True,
        )

        return deletedColumn.item

    def modify(
        self,
        index: int,
        item: Item,
    ) -> None:
        global _store

        _store[index] = _Column(
            item=item,
            logical_deleted=False,
        )

    def findAll(
        self,
    ) -> Dict[int, Item]:
        global _store
        return {key: value.item for key, value in _store.items()}
