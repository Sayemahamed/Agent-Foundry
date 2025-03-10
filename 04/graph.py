from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph.state import CompiledStateGraph
from state04 import State
from Nodes04 import call_agent, summarize, decider


builder = StateGraph(state_schema=State)

builder.add_node(node="agent", action=call_agent)
builder.add_node(node="summarize", action=summarize)

builder.add_conditional_edges(source=START, path=decider)
builder.add_edge(start_key="summarize", end_key="agent")
builder.add_edge(start_key="agent", end_key=END)
with PostgresSaver.from_conn_string(
    "postgresql://postgres:postgres@localhost:5432/postgres"
) as memory:
    graph: CompiledStateGraph = builder.compile(
        interrupt_before=["summarize"], checkpointer=memory
    )

# graph.invoke(
#     {"messages": [HumanMessage(content="Hello, I am Sayem")]},
#     {"configurable": {"thread_id": 1}},
# )
# graph.invoke(
#     {"messages": [HumanMessage(content="can You Help me with maths")]},
#     {"configurable": {"thread_id": 1}},
# )
# graph.invoke(
#     {"messages": [HumanMessage(content="who are You?")]},
#     {"configurable": {"thread_id": 1}},
# )
