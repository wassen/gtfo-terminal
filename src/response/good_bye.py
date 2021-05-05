from . import Response


class GoodByeResponse(Response):
    # should_close: bool = True

    def response_string(self) -> str:
        return "UPLINK DISCONNECTED"
