from typing import Optional

# 選択肢とアイテムの種類は別な気がするが、二重に定義するのもなあ
# 選択肢がEnumじゃなくて、特定のリストを返すProtocolなら良いのかな・・・
# 選択肢の結果ともとれるか？うーん
from ..response.choices import AddContainerTypeChoice, AddItemTypeChoice


class Item:
    item_type: AddItemTypeChoice
    item_count: int
    zone_number: Optional[int]
    container_type: Optional[AddContainerTypeChoice]
    container_number: Optional[int]

    class Builder:
        item_type: Optional[AddItemTypeChoice]
        item_count: Optional[int]
        zone_number: Optional[int]
        container_type: Optional[AddContainerTypeChoice]
        container_number: Optional[int]

        def build(self) -> "Item":
            return Item(self)

    # いい感じに全列をフォーマットさせたい
    def __str__(self) -> str:
        return f"|{self.item_type.short_name}: {self.item_count}|zone: {self.zone_number}|{self.container_type.itemName}: {self.container_number}|"

    # def __init__(self, builder: Builder):
    #     if not builder.item_type:
    #         raise Exception()
    #     if not builder.item_count:
    #         raise Exception()
    #     self.item_type = builder.item_type
    #     self.item_count = builder.item_count
    #     self.zone_number = builder.zone_number
    #     self.container_type = builder.container_type
    #     self.container_number = builder.container_number
