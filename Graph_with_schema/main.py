import random
from pydantic import BaseModel, field_validator, ValidationError
from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image
from typing import Literal


class State(BaseModel):
    name: str
    mood: str

    @field_validator("mood")
    @classmethod
    def validate_mood(cls, value):
        if value not in ["happy", "sad"]:
            raise ValueError("mood must be either 'happy' or 'sad'")
        return value


def node_1(state: State) -> State:
    print("---Node 1---")
    state.name = "I am " + state.name
    return state


def node_2(state: State) -> State:
    print("---Node 2---")
    state.mood = "Happy."
    return state


def node_3(state: State) -> State:
    print("---Node 3---")
    state.mood = "Sad."
    return state


def decider(state: State) -> Literal["Node2", "Node3"]:
    return random.choice(["Node2", "Node3"])


builder = StateGraph(State)
builder.add_node("Node1", node_1)
builder.add_node("Node2", node_2)
builder.add_node("Node3", node_3)

builder.add_edge(START, "Node1")
builder.add_conditional_edges("Node1", decider)
builder.add_edge("Node2", END)
builder.add_edge("Node3", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

graph.invoke({"name": "Sayem", "mood": "happy"})
