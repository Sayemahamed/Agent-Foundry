from state02 import State
from langgraph.graph import START, END, StateGraph
from Nodes02 import Node_1, Node_2, Node_3, Node_4


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

graph = builder.compile()
