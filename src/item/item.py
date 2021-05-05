from typing import Optional

# 選択肢とアイテムの種類は別な気がするが、二重に定義するのもなあ
# 選択肢がEnumじゃなくて、特定のリストを返すProtocolなら良いのかな・・・
# 選択肢の結果ともとれるか？うーん
from ..response.choices import AddContainerTypeChoice, AddItemTypeChoice


class Item:
    item_type: Optional[AddItemTypeChoice]
    item_count: Optional[int]
    zone_number: Optional[int]
    container_type: Optional[AddContainerTypeChoice]
    container_number: Optional[int]
