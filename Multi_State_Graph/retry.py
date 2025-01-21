from IPython.display import display, Image
from annotated_types import UpperCase
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class GlobalState(TypedDict):
    public_data: str

class PrivetState(TypedDict):
    privet_data: str

def Node1(data: GlobalState) -> PrivetState:
    print("---NODE 1---")
    data["public_data"]=data["public_data"].capitalize()
    return {"privet_data": data["public_data"] + " -> node 1 "}

def Node2(data: PrivetState) -> GlobalState:
    print("---NODE 2---")
    return {"public_data": data["privet_data"] + " -> node 2"}


builder = StateGraph(GlobalState)
builder.add_node("Node1", Node1)
builder.add_node("Node2", Node2)

builder.add_edge(START, "Node1")
builder.add_edge("Node1", "Node2")
builder.add_edge("Node2", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

graph.invoke({"public_data": "hi"})