from typing import TypedDict, Annotated
from langgraph.graph import START, END, StateGraph
from operator import add
from IPython.display import display, Image


class State(TypedDict):
    count: Annotated[list[int], add]


def node_1(state: State) -> State:
    return {"count": [state["count"][-1] + 1]}


def node_2(state: State) -> State:
    return {"count": [state["count"][-1] + 1]}


def node_3(state: State) -> State:
    return {"count": [state["count"][-1] + 1]}


builder1 = StateGraph(State)
builder1.add_node("node_1", node_1)
builder1.add_node("node_2", node_2)
builder1.add_node("node_3", node_3)

builder1.add_edge(START, "node_1")
builder1.add_edge("node_1", "node_2")
builder1.add_edge("node_1", "node_3")
builder1.add_edge("node_2", END)
builder1.add_edge("node_3", END)

graph_1 = builder1.compile()
display(Image(graph_1.get_graph().draw_mermaid_png()))

graph_1.invoke({"count": [1]})
