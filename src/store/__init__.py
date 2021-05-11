from typing import Dict, Optional

from ..item.item import Item


class Store:
    # def clear(
    #     self,
    # ) -> None:
    #     raise NotImplementedError()

    def add(
        self,
        item: Item,
    ) -> int:
        raise NotImplementedError()

    def drop(
        self,
        index: int,
    ) -> Optional[Item]:
        raise NotImplementedError()

    def modify(
        self,
        index: int,
        item: Item,
    ) -> None:
        raise NotImplementedError()

    def restore(
        self,
        index: int,
    ) -> Optional[Item]:

        raise NotImplementedError()

    def findAll(
        self,
    ) -> Dict[int, Item]:
        raise NotImplementedError()
