import random
from pydantic import BaseModel ,field_validator,ValidationError
from langgraph.graph import StateGraph,START,END
from IPython.display import display,Image
from typing import Literal

class State(BaseModel):
    name: str
    mood: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return value
    
def Node1(state:State)->State:
    print("---Node 1---")
    state.name = "I am " + state.name
    return state


def Node2(state:State)->State:
    print("---Node 2---")
    state.mood = "Happy."
    return state


def Node3(state:State)->State:
    print("---Node 3---")
    state.mood = "Sad."
    return state


def decider(state:State)->Literal["Node2","Node3"]:
    # Often used for decision making
    return random.choice(["Node2","Node3"])


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

graph.invoke({"name": "Sayem", "mood": ""})
