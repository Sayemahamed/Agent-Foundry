from langgraph.graph import START, StateGraph
from regex import P
from state08 import State
from Nodes08 import initial, intermediate, final
from langgraph.checkpoint.postgres import PostgresSaver
from rich import print
# from langgraph.store.postgres import PostgresStore

builder = StateGraph(State)

builder.add_node("initial", initial)
builder.add_node("intermediate", intermediate)
builder.add_node("final", final)

builder.add_edge(START, "initial")
# graph = builder.compile()
with PostgresSaver.from_conn_string(
    "postgresql://postgres:postgres@localhost:5432/postgres"
) as memory:
    memory.setup()
    graph = builder.compile(checkpointer=memory)
    # graph.invoke( input={"initialS": "1A"}, config={"configurable": {"thread_id": "1"}})

    # graph.update_state(config={"configurable": {"thread_id": "1", 'checkpoint_id': '1effa5a0-9bab-628e-bfff-e4b253dcbdf7'}},values={"initialS": "1A"})

    # graph.invoke(None,{"configurable": {"thread_id": "1", 'checkpoint_id': '1effa5a0-9bab-628e-bfff-e4b253dcbdf7'}})

    state_history = graph.get_state_history(config={"configurable": {"thread_id": "1"}})
    for state in state_history:
        print(state)
