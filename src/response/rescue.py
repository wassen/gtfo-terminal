from . import Response


class RescueResponse(Response):
    def response_string(self) -> str:
        return f"アイテムを元に戻しました。以前の状態に戻す場合は以下のコマンドを入力してください\n`rescue {self.random_hash}`"

    def __init__(self, random_hash: str) -> None:
        self.random_hash = random_hash
