from typing import TypedDict
from IPython.display import display, Image
from langgraph.graph import START, END, StateGraph


class GlobalState(TypedDict):
    public_data: str


class PrivetState(TypedDict):
    privet_data: str


def node_1(data: GlobalState) -> PrivetState:
    print("---NODE 1---")
    return {"privet_data": data["public_data"] + " -> node 1"}


def node_2(data: PrivetState) -> GlobalState:
    print("---NODE 2---")
    return {"public_data": data["privet_data"] + " -> node 2"}


builder = StateGraph(GlobalState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
graph.invoke({"public_data": "hi"})


# ------
