from state02 import State


def Node_1(state: State) -> State:
    print("---Node_1---")
    return {"count": [state["count"][-1] + 1]}


def Node_2(state: State) -> State:
    print("---Node_2---")
    return {"count": [state["count"][-1] + 1]}


def Node_3(state: State) -> State:
    print("---Node_3---")
    return {"count": [state["count"][-1] + 1]}


def Node_4(state: State) -> State:
    print("---Node_4---")
    return {"count": [state["count"][-1] + 1]}
