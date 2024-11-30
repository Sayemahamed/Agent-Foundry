from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Literal
import random


class State(TypedDict):
    graph_state: str
    name: str


def node_1(state: State) -> State:
    print("---Node 1---")
    return {"graph_state": state["graph_state"] + " I Am", "name": state["name"]}


def node_2(state: State) -> State:
    print("---Node 2---")
    return {"graph_state": state["graph_state"] + " Happy", "name": state["name"]}


def node_3(state: State) -> State:
    print("---Node 3---")
    return {"graph_state": state["graph_state"] + " Sad", "name": state["name"]}


def decider(state: State) -> Literal["node_2", "node_3"]:
    return random.choice(["node_2", "node_3"])


builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decider)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)
graph = builder.compile()

graph.invoke({"graph_state": "Hello, I am Sayem", "name": "Sayem"})
