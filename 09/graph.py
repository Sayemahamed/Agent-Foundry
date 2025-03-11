from langgraph.graph import START, StateGraph
from state09 import State
from Nodes09 import initial, intermediate, final
from langgraph.checkpoint.postgres import PostgresSaver
from rich import print
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

builder = StateGraph(State)

builder.add_node("initial", initial)
builder.add_node("intermediate", intermediate)
builder.add_node("final", final)

builder.add_edge(START, "initial")
graph = builder.compile(checkpointer=MemorySaver())

# async for chunk in graph.astream(
#     input={"initialS": "1A"}, config={"configurable": {"thread_id": "1"}}
# ):
#     print(chunk)

# async for chunk in graph.astream(
#     Command(resume="1B"), config={"configurable": {"thread_id": "1"}}
# ):
#     print(chunk)
