from enum import Enum, auto
from typing import List

from . import Response


class ClearResponse(Response):
    def response_string(self) -> str:
        return f"全てのアイテムを削除しました。もとに戻す場合は以下のコマンドを入力してください\n`rescue {self.random_hash}`"

    def __init__(self, random_hash: str) -> None:
        self.random_hash = random_hash
