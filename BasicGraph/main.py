from typing import TypedDict, Literal
import random
from IPython.display import display, Image


class State(TypedDict):
    graph_state: str


def Node1(state: State) -> State:
    print("---Node 1---")
    return {"graph_state": state["graph_state"] + " I am"}


def Node2(state: State) -> State:
    print("---Node 2---")
    return {"graph_state": state["graph_state"] + " Happy."}


def Node3(state: State) -> State:
    print("---Node 3---")
    return {"graph_state": state["graph_state"] + " Sad."}


def decider(state: State) -> Literal["Node2", "Node3"]:
    # Often used for decision making
    user_input = state["graph_state"]

    return random.choice(["Node2", "Node3"])
