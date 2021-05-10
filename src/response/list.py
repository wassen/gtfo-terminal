from typing import Callable, Dict, List, Tuple

from ..item.item import Item
from . import Response
from .choices import AddContainerTypeChoice


class ListResponse(Response):
    items: Dict[int, Item]

    def response_string(self) -> str:
        return self.format(self.items)

    def __init__(
        self,
        items: Dict[int, Item],
    ):
        self.items = items

    def __spaces(self, count: int) -> str:
        return " " * count

    # 返り値が良くない、というか加算した長さ返す必要ある？
    # 渡すものも大きすぎるか？
    def __item_length(
        self,
        items: Dict[int, Item],
    ) -> Tuple[int, int, int]:
        max_item_type_length: int = max(
            [len(item.item_type.short_name) for item in items.values()]
        )

        max_item_count_length: int = max(
            [len(str(item.item_count)) for item in items.values()]
        )
        return (
            max_item_type_length,
            max_item_count_length,
            (max_item_type_length + 2 + max_item_count_length),
        )

    def __zone_length(
        self,
        items: Dict[int, Item],
    ) -> Tuple[int, int]:

        zone_numbers = [
            item.zone_number for item in items.values() if item.zone_number is not None
        ]
        if len(zone_numbers) == 0:
            max_zone_number_length = 0
        else:
            max_zone_number_length = max(
                [len(str(zone_number)) for zone_number in zone_numbers]
            )
        if max_zone_number_length == 0:
            return 0, 0
        else:
            # "zone: " で6
            return max_zone_number_length, 6 + max_zone_number_length

    def __container_length(
        self,
        items: Dict[int, Item],
    ) -> Tuple[int, int, int]:

        container_types: List[AddContainerTypeChoice] = [
            item.container_type
            for item in items.values()
            if item.container_type is not None
        ]

        if len(container_types) == 0:
            return 0, 0, 0
        else:
            max_container_type_length: int = max(
                [len(container_type.short_name) for container_type in container_types]
            )

        container_numbers: List[int] = [
            item.container_number
            for item in items.values()
            if item.container_number is not None
        ]

        if len(container_numbers) == 0:
            max_container_number_length = 0
        else:
            max_container_number_length = max(
                [len(str(container_nubmer)) for container_nubmer in container_numbers]
            )

        if max_container_number_length == 0:
            return 0, 0, 0
        else:
            return (
                max_container_type_length,
                max_container_number_length,
                max_container_type_length + 2 + max_container_number_length,
            )

    def __item_type_string(self, value: Item, max_item_type_length: int) -> str:
        return f"{self.__spaces(max_item_type_length - len(value.item_type.short_name))}{value.item_type.short_name}: "

    def __item_count_string(self, value: Item, max_item_count_length: int) -> str:
        return f"{value.item_count:{max_item_count_length}d}"

    def __zone_string(self, value: Item, max_zone_number_length: int) -> str:
        # unwrapしてから渡したい
        return f"zone: {value.zone_number:{max_zone_number_length}d}"

    def __container_type_string(
        self, value: Item, max_container_type_length: int
    ) -> str:
        return f"{self.__spaces(max_container_type_length - len(value.container_type.short_name))}{value.container_type.short_name}: "

    def __container_number_string(
        self, value: Item, max_container_number_length: int
    ) -> str:
        return f"{value.container_number:{max_container_number_length}d}"

    def format(
        self,
        items: Dict[int, Item],
    ) -> str:
        if len(items.items()) == 0:
            return "No items"

        (max_item_type_length, max_item_count_length, item_length) = self.__item_length(
            items
        )

        (max_zone_number_length, zone_length) = self.__zone_length(items)

        (
            max_container_type_length,
            max_container_number_length,
            container_length,
        ) = self.__container_length(items)

        return "\n".join(
            ["```"]
            + [
                f"x|{self.__spaces(item_length)}|{self.__spaces(zone_length)}|{self.__spaces(container_length)}|"
            ]
            + [
                (
                    f"{key}|"
                    f"{self.__item_type_string(value, max_item_type_length)}"
                    f"{self.__item_count_string(value, max_item_count_length)}|"
                    f"{self.__zone_string(value, max_zone_number_length) if value.zone_number is not None else self.__spaces(zone_length)}|"
                    f"{self.__container_type_string(value, max_container_type_length) if value.container_type is not None else self.__spaces(container_length)}"
                    f"{self.__container_number_string(value, max_container_number_length) if value.container_number is not None else ''}|"
                )
                for key, value in items.items()
            ]
            + ["```"]
        )
