from langgraph.graph import START, END, StateGraph
from state05 import State
from langgraph.store.postgres import PostgresStore
from psycopg_pool import ConnectionPool
from langchain_core.runnables  import RunnableConfig 
from langgraph.checkpoint.postgres import PostgresSaver
from Nodes05 import call

builder = StateGraph(State)
builder.add_node("call", call)
builder.add_edge(START, "call")

# with ConnectionPool(conninfo="postgresql://postgres:postgres@localhost:5432/postgres") as pool:
#     with pool.connection() as conn:
#         conn.autocommit = True  # Enable autocommit mode
#         store = PostgresStore(conn)
#         store.setup()
#         # ... rest of your code ...


with ConnectionPool(conninfo="postgresql://postgres:postgres@localhost:5432/postgres") as pool:
    with pool.connection() as conn:
        checkpointer = PostgresSaver(conn)
        store = PostgresStore(conn)
        graph = builder.compile(checkpointer=checkpointer, store=store)
        input_message ={"role": "user", "content": "Hi! Remember: my name is Sayem"}
        response=graph.invoke({"messages":input_message},RunnableConfig(configurable={"user_id": "Sayem", "thread_id": "1"}))
        for message in response["messages"]:
            message.pretty_print()
        input_message ={"role": "user", "content": "What is my Name?"}
        response=graph.invoke({"messages":input_message},RunnableConfig(configurable={"user_id": "Sayem", "thread_id": "2"}))
        for message in response["messages"]:
            message.pretty_print()
