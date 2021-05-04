from typing import Optional, TypeVar, cast

T = TypeVar("T")


def unwrap(value: Optional[T]) -> T:
    if value is None:
        raise Exception()

    # 何故castがいらないのか
    return value
