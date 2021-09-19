from enum import Enum, auto
from typing import List

from . import Response

# Addとかなり似通っているので共通化できそうではある


class SelectResponse(Response):
    complete = False


class SelectEditResponse(SelectResponse):
    def response_string(self) -> str:
        items_string: List[str] = [
            f"{item.value}: {item.itemName}" for item in list(SelectEditChoice)
        ]
        combined_string: str = "\n".join(items_string)
        with_code_block = f"```\n{combined_string}\n```"
        return f"何を編集しますか？数値を入力してください\n{with_code_block}"


class SelectCompleteResponse(SelectResponse):
    complete = True

    def response_string(self) -> str:
        return f"完了しました"


class SelectState:
    # idleはAddStateじゃないような
    idle = auto()
    edit = auto()
    zone_number = auto()
    container_type = auto()
    container_number = auto()
    item_count = auto()

    def response(self) -> Response:
        if self == SelectState.idle:
            return SelectCompleteResponse()
        elif self == SelectState.item_count:
            return SelectItemCountResponse()
        elif self == SelectState.edit:
            return SelectEditResponse()
        elif self == SelectState.zone_number:
            return SelectZoneNumberResponse()
        elif self == SelectState.container_type:
            return SelectContainerTypeResponse()
        elif self == SelectState.container_number:
            return SelectContainerNumberResponse()
        else:
            raise Exception()


class SelectEditChoice(Enum):
    # complete = 0
    # zone = 1
    # container = 2
    # item_count = 3
    delete = 4

    @property
    def screen_name(self) -> str:
        # if self == self.complete:
        #     return "終了"
        # elif self == self.zone:
        #     return "ゾーン"
        # elif self == self.container:
        #     return "入れ物"
        # elif self == self.item_count:
        #     return "アイテムの数"
        if self == self.delete:
            return "削除"
        else:
            raise Exception()

    def next_state(self) -> SelectState:
        if self == AddEditChoice.complete:
            return AddState.idle
        elif self == AddEditChoice.zone:
            return AddState.zone_number
        elif self == AddEditChoice.container:
            return AddState.container_type
        elif self == AddEditChoice.item_count:
            return AddState.item_count
        else:
            raise Exception()
