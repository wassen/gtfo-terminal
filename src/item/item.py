from typing import Optional

from ..item_property import ItemType


class Item:
    item_type: Optional[ItemType]
    item_count: Optional[int]
    zone_number: Optional[int]
    container_type: Optional[str]
    container_number: Optional[str]
