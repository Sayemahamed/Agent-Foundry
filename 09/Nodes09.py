import random
from state09 import State
from langgraph.types import Command
from typing import Literal
from langgraph.func import entrypoint, task
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver


@task
def make_a_choice(stage: str):
    print("---make_a_choice---")
    choice = interrupt(
        {
            "stage": stage,
            "action": "make a choice",
        }
    )
    return choice


@entrypoint(checkpointer=MemorySaver())
def initial(state: State) -> Command[Literal["intermediate"]]:
    print("---initial---")
    response: str = random.choice(["1A", "1B"])

    # ======================== make a choice =========================
    choice = make_a_choice("initial").result()
    print(choice)
    print(response)
    if response == choice:
        print("Hurrah!")
    else:
        print("Boo!")
    # ======================== make a choice =========================

    return Command(
        update={"initialS": response},
        goto="intermediate",
    )


# async for chunk in initial.astream(input="cat", config={"configurable": {"thread_id": "1"}}):
#     print(chunk)

# async for chunk in initial.astream(Command(resume="1B"), config={"configurable": {"thread_id": "1"}}):
#     print(chunk)


@entrypoint(checkpointer=MemorySaver())
def intermediate(state: State) -> Command[Literal["final"]]:
    print("---intermediate---")
    if state.initialS == "1A":
        response: str = random.choice(["2A", "2B"])
    else:
        response: str = random.choice(["2C", "2D"])

    # ======================== make a choice =========================
    choice = make_a_choice("intermediate").result()
    print(choice)
    print(response)
    if response == choice:
        print("Hurrah!")
    else:
        print("Boo!")
    # ======================== make a choice =========================

    return Command(
        update={"intermediateS": response},
        goto="final",
    )


@entrypoint(checkpointer=MemorySaver())
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

    # ======================== make a choice =========================
    choice = make_a_choice("final").result()
    print(choice)
    print(response)
    if response == choice:
        print("Hurrah!")
    else:
        print("Boo!")
    # ======================== make a choice =========================

    return Command(
        update={"finalS": response},
        goto="__end__",
    )
