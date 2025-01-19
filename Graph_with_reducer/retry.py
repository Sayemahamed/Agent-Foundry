from typing import TypedDict,Annotated
from langgraph.graph import START, END, StateGraph
from IPython.display import display, Image
from operator import add

class State(TypedDict):
    count : Annotated[list[int],add]

def Node1(state:State)->State:
    return {"count": [state["count"][-1] + 1]}

def Node2(state:State)->State:
    return{"count": [state["count"][-1] + 1]}

def Node3(state:State)->State:
    return{"count": [state["count"][-1] + 1]}

builder = StateGraph(State)

builder.add_node("Node1", Node1)
builder.add_node("Node2", Node2)
builder.add_node("Node3", Node3)

builder.add_edge(START, "Node1")
builder.add_edge("Node1", "Node2")
builder.add_edge("Node1", "Node3")
builder.add_edge("Node2", END)
builder.add_edge("Node3", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

graph.invoke({"count": [-1]})


# -------------------------Custom Reducer-------------------------------

def reduce_list(Left:list|None,Right:list|None)->list:
    if not Left:
        Left = [0]
    if not Right:
        Right = []
    return Left + Right


class CustomState(TypedDict):
    count: Annotated[list[int], reduce_list]

def Node1(state:CustomState)->CustomState:
    return {"count": [state["count"][-1] + 1]}

def Node2(state:CustomState)->CustomState:
    return{"count": [state["count"][-1] + 1]}

def Node3(state:CustomState)->CustomState:
    return{"count": [state["count"][-1] + 1]}

builder1 = StateGraph(CustomState)

builder1.add_node("Node1", Node1)
builder1.add_node("Node2", Node2)
builder1.add_node("Node3", Node3)

builder1.add_edge(START, "Node1")
builder1.add_edge("Node1", "Node2")
builder1.add_edge("Node1", "Node3")
builder1.add_edge("Node2", END)
builder1.add_edge("Node3", END)

graph_1 = builder1.compile()

display(Image(graph_1.get_graph().draw_mermaid_png()))

graph_1.invoke({"count": [-1]})  