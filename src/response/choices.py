from enum import Enum, auto
from typing import List, Optional, Type

from . import Response


class AddZoneNumberResponse(Response):
    def response_string(self) -> str:
        return "ゾーン番号はいくつですか？数値を入力してください"


class AddItemTypeResponse(Response):
    def response_string(self) -> str:
        items_string: List[str] = [
            f"{item.value: >2}: {item.itemName}" for item in list(AddItemTypeChoice)
        ]
        combined_string: str = "\n".join(items_string)
        with_code_block = f"```\n{combined_string}\n```"
        return f"どのアイテムを保管しますか？数値を入力してください\n{with_code_block}"


class AddItemCountResponse(Response):
    def response_string(self) -> str:
        return "何個入りですか？数値を入力してください"


class AddInAdditionResponse(Response):
    def response_string(self) -> str:
        return "アイテム追加中です"


class AddEditResponse(Response):
    def response_string(self) -> str:
        items_string: List[str] = [
            f"{item.value}: {item.itemName}" for item in list(AddEditChoice)
        ]
        combined_string: str = "\n".join(items_string)
        with_code_block = f"```\n{combined_string}\n```"
        return f"何を編集しますか？数値を入力してください\n{with_code_block}"


class AddContainerTypeResponse(Response):
    def response_string(self) -> str:
        items_string: List[str] = [
            f"{item.value: >2}: {item.itemName}"
            for item in list(AddContainerTypeChoice)
        ]
        combined_string: str = "\n".join(items_string)
        with_code_block = f"```\n{combined_string}\n```"
        return f"入れ物のタイプを数値を入力してください\n{with_code_block}"


class AddContainerNumberResponse(Response):
    def response_string(self) -> str:
        return f"入れ物の番号はいくつですか？数値で入力してください（直置きのときもなんか入力しといて）"


class AddState(Enum):
    item_type = auto()
    item_count = auto()
    edit = auto()
    zone_number = auto()
    container_type = auto()
    container_number = auto()

    def response(self) -> str:
        if self == AddState.item_type:
            return AddItemTypeResponse().response_string()
        elif self == AddState.item_count:
            return AddItemCountResponse().response_string()
        elif self == AddState.edit:
            return AddEditResponse().response_string()
        elif self == AddState.zone_number:
            return AddZoneNumberResponse().response_string()
        elif self == AddState.container_type:
            return AddContainerTypeResponse().response_string()
        elif self == AddState.container_number:
            return AddContainerNumberResponse().response_string()
        else:
            raise Exception()


class Choice:
    pass

    @property
    def itemName(self) -> str:
        raise Exception()


class AddItemTypeChoice(Choice, Enum):
    ammo = 1
    medi = 2
    tool = 3
    disinfection = 4
    fog_repeller = 5
    long_range_flashlight = 6
    c_form_granade = 7
    lock_melter = 8
    glow_stick = 9
    l2_lp_syringe = 10
    iix_syringe = 11
    explosive_tripmine = 12
    c_form_tripmine = 13

    @property
    def itemName(self) -> str:
        if self == AddItemTypeChoice.ammo:
            return "Ammunition Pack"
        elif self == AddItemTypeChoice.medi:
            return "Medical Pack"
        elif self == AddItemTypeChoice.tool:
            return "Tool Refill Pack"
        elif self == AddItemTypeChoice.disinfection:
            return "Disinfection Pack"
        elif self == AddItemTypeChoice.fog_repeller:
            return "Fog Repeller"
        elif self == AddItemTypeChoice.long_range_flashlight:
            return "Long Range Flashlight"
        elif self == AddItemTypeChoice.c_form_granade:
            return "C-form Granade"
        elif self == AddItemTypeChoice.lock_melter:
            return "Lock Melter"
        elif self == AddItemTypeChoice.glow_stick:
            return "Glow Stick"
        elif self == AddItemTypeChoice.l2_lp_syringe:
            return "L2 LP Syringe"
        elif self == AddItemTypeChoice.iix_syringe:
            return "IIX Syringe"
        elif self == AddItemTypeChoice.explosive_tripmine:
            return "Explosive Tripmine"
        elif self == AddItemTypeChoice.c_form_tripmine:
            return "C-form Tripmine"
        else:
            raise Exception()


class AddEditChoice(Choice, Enum):
    complete = 0
    zone = 1
    container = 2
    item_count = 3

    # 外向けの名前、もっといい命名がほしい
    @property
    def itemName(self) -> str:
        if self == AddEditChoice.complete:
            return "終了"
        elif self == AddEditChoice.zone:
            return "ゾーン"
        elif self == AddEditChoice.container:
            return "入れ物"
        elif self == AddEditChoice.item_count:
            return "アイテムの数"
        else:
            raise Exception()

    def next_state(self) -> Optional[AddState]:
        if self == AddEditChoice.complete:
            # Noneじゃなくて平常時も状態として管理しない？
            return None
        elif self == AddEditChoice.zone:
            return AddState.zone_number
        elif self == AddEditChoice.container:
            return AddState.container_type
        elif self == AddEditChoice.item_count:
            return AddState.item_count
        else:
            raise Exception()


class AddContainerTypeChoice(Choice, Enum):
    box = auto()
    locker = auto()
    others = auto()

    @property
    def itemName(self) -> str:
        if self == AddContainerTypeChoice.box:
            return "ボックス"
        elif self == AddContainerTypeChoice.locker:
            return "ロッカー"
        elif self == AddContainerTypeChoice.others:
            return "直置き"
        else:
            raise Exception()


# matrix?
def from_state_to_choice(state: AddState) -> Optional[Type[Choice]]:
    if AddState.item_type:
        return AddItemTypeChoice
    elif AddState.item_count:
        return None
    elif AddState.edit:
        return AddEditChoice
    elif AddState.zone_number:
        return None
    elif AddState.container_type:
        return AddContainerTypeChoice
    elif AddState.container_number:
        return None
    else:
        raise Exception()
