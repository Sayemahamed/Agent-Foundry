from typing import Annotated, TypedDict


def custom_reducer(left: list[int], right: list[int]) -> list[int]:
    if not left:
        left = []
    if not right:
        right = [0]
    return left + right


class State(TypedDict):
    count: Annotated[list[int], custom_reducer]
