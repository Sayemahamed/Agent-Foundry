import random
from state08 import State
from langgraph.types import Command
from typing import Literal


def initial(state: State) -> Command[Literal["intermediate"]]:
    print("---initial---")
    response: str = random.choice(["1A", "1B"])
    return Command(
        update={"initialS": response},
        goto="intermediate",
    )


def intermediate(state: State) -> Command[Literal["final"]]:
    print("---intermediate---")
    if state.initialS == "1A":
        response: str = random.choice(["2A", "2B"])
    else:
        response: str = random.choice(["2C", "2D"])
    return Command(
        update={"intermediateS": response},
        goto="final",
    )


def final(state: State) -> Command[Literal["__end__"]]:
    print("---final---")
    if state.intermediateS == "2A":
        response: str = random.choice(["3A", "3B"])
    elif state.intermediateS == "2B":
        response: str = random.choice(["3C", "3D"])
    elif state.intermediateS == "2C":
        response: str = random.choice(["3E", "3F"])
    else:
        response: str = random.choice(["3G", "3H"])
    return Command(
        update={"finalS": response},
        goto="__end__",
    )
