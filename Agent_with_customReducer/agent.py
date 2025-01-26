from state import State
from langgraph.graph import START, END,StateGraph

def Node_1(state: State) -> State:
    print("---Node_1---")
    return {"count": [state["count"][-1]+1]}

def Node_2(state: State) -> State:
    print("---Node_2---")
    return {"count":[state["count"][-1]+1]}

def Node_3(state: State) -> State:
    print("---Node_3---")
    return {"count":[state["count"][-1]+1]}

def Node_4(state: State) -> State:
    print("---Node_4---")
    return {"count":[state["count"][-1]+1]}


builder = StateGraph(State)

builder.add_node("Node_1", Node_1)
builder.add_node("Node_2", Node_2)
builder.add_node("Node_3", Node_3)
builder.add_node("Node_4", Node_4)

builder.add_edge(START, "Node_1")
builder.add_edge("Node_1", "Node_2")
builder.add_edge("Node_1", "Node_3")
builder.add_edge("Node_2", "Node_4")
builder.add_edge("Node_3", "Node_4")
builder.add_edge("Node_4", END)

graph=builder.compile()