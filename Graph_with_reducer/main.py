from pickle import BUILD
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

# -------------------------Custom Reducer-------------------------------


def reduce_list(left: list | None, right: list | None) -> list:
    if not left:
        left = [0]
    if not right:
        right = []
    return left + right


class CustomState(TypedDict):
    count: Annotated[list[int], reduce_list]


def node_1(state: CustomState) -> CustomState:
    return {"count": [state["count"][-1] + 1]}


def node_2(state: CustomState) -> CustomState:
    return {"count": [state["count"][-1] + 1]}


def node_3(state: CustomState) -> CustomState:
    return {"count": [state["count"][-1] + 1]}


builder2 = StateGraph(CustomState)
builder2.add_node("node_1", node_1)
builder2.add_node("node_2", node_2)
builder2.add_node("node_3", node_3)

builder2.add_edge(START, "node_1")
builder2.add_edge("node_1", "node_2")
builder2.add_edge("node_1", "node_3")
builder2.add_edge("node_2", END)
builder2.add_edge("node_3", END)

graph_2 = builder2.compile()
display(Image(graph_2.get_graph().draw_mermaid_png()))

graph_2.invoke({"count":[]})
