from typing import Literal
from state01 import State
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnableLambda

# Define your nodes (tasks)
def Node_1(state: State) -> State:
    print("---Node_1---")
    return {"state": "I am " + state["state"] + "."}

def Node_2(state: State) -> State:
    print("---Node_2---")
    return {"state": state["state"] + " I am Happy."}

def Node_3(state: State) -> State:
    print("---Node_3---")
    return {"state": state["state"] + " I am Sad."}

# Combine Node_2 and Node_3 in parallel
parallel_tasks = RunnableParallel(
    {
        "node_2_output": RunnableLambda(Node_2),
        "node_3_output": RunnableLambda(Node_3),
    }
)

# Create the graph
builder = StateGraph(State)

builder.add_node("Node_1", Node_1)
builder.add_node("Parallel_Node", parallel_tasks)

builder.add_edge(START, "Node_1")
builder.add_edge("Node_1", "Parallel_Node")
builder.add_edge("Parallel_Node", END)

graph = builder.compile()

# Example execution
state = {"state": "starting state"}
result = graph.invoke(state)
print(result)
