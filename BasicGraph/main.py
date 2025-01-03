from typing import TypedDict, Literal
import random
from IPython.display import display, Image
from langgraph.graph import START, END, StateGraph


class State(TypedDict):
    graph_state: str
    name: str


def Node1(state: State) -> State:
    print("---Node 1---")
    return {"graph_state": state["graph_state"] + " I am", "name": state["name"]}


def Node2(state: State) -> State:
    print("---Node 2---")
    return {"graph_state": state["graph_state"] + " Happy.", "name": state["name"]}


def Node3(state: State) -> State:
    print("---Node 3---")
    return {"graph_state": state["graph_state"] + " Sad.", "name": state["name"]}


def decider(state: State) -> Literal["Node2", "Node3"]:
    # Often used for decision making
    user_input = state["graph_state"]

    return random.choice(["Node2", "Node3"])


builder = StateGraph(State)

builder.add_node("Node1", Node1)
builder.add_node("Node2", Node2)
builder.add_node("Node3", Node3)

builder.add_edge(START, "Node1")
builder.add_conditional_edges("Node1", decider)
builder.add_edge("Node2", END)
builder.add_edge("Node3", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))


graph.invoke({"graph_state": "Hello, I am Sayem.", "name": "Sayem"})
