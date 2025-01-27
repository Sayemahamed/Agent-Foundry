from turtle import st
from typing import Literal
import random
from IPython.display import Image, display
from src.agent.state import State
from langgraph.graph import START, END, StateGraph


def Node_1(state: State) -> State:
    print("---Node_1---")
    return {"state": "I am " + state["state"] + "."}


def Node_2(state: State) -> State:
    print("---Node_2---")
    return {"state": state["state"] + "I am Happy."}


def Node_3(state: State) -> State:
    print("---Node_3---")
    return {"state": state["state"] + "I am Sad."}


def decider(state: State) -> Literal["Node_2", "Node_3"]:
    print("---decider---")
    return random.choice(["Node_2", "Node_3"])


builder = StateGraph(State)

builder.add_node("Node_1", Node_1)
builder.add_node("Node_2", Node_2)
builder.add_node("Node_3", Node_3)

builder.add_edge(START, "Node_1")
builder.add_conditional_edges("Node_1", decider)
builder.add_edge("Node_2", END)
builder.add_edge("Node_3", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
