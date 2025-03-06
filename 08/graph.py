from langgraph.graph import START, StateGraph
from state08 import State
from Nodes08 import initial, intermediate, final
from langgraph.checkpoint.postgres import PostgresSaver
# from langgraph.store.postgres import PostgresStore

builder = StateGraph(State)

builder.add_node("initial", initial)
builder.add_node("intermediate", intermediate)
builder.add_node("final", final)

builder.add_edge(START, "initial")
graph = builder.compile()
# with PostgresSaver.from_conn_string(
#     "postgresql://postgres:postgres@localhost:5432/postgres"
# ) as memory:
#     graph = builder.compile(checkpointer=memory)
#     graph.invoke({"output":0}, {"configurable": {"thread_id": "1"}})