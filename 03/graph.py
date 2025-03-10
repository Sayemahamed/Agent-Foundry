from langgraph.graph import START, END, StateGraph
from state03 import State
from langgraph.prebuilt import ToolNode, tools_condition
from tools03 import *
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres import PostgresSaver
from Nodes03 import call_agent





builder = StateGraph(State)

builder.add_node("agent", call_agent)
builder.add_node(
    "tools", ToolNode([multiply, divide, add, subtract, power, sqrt, factorial])
)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.add_edge("agent", END)
with PostgresSaver.from_conn_string(
    "postgresql://postgres:postgres@localhost:5432/postgres"
) as memory:
    graph = builder.compile(interrupt_before=["tools"], checkpointer=memory)

# for event in graph.stream(
#     input={"messages": [HumanMessage(content="what is 2+2?")]},
#     config={"configurable": {"thread_id": 1}},
#     stream_mode="values"
# ):
#     event["messages"][-1].pretty_print()

# It will continue after the interrupt (before the "tools" node)

# for event in graph.stream(
#     input=None, # Input should be None to continue after the interrupt
#     config={"configurable": {"thread_id": 1}},
#     stream_mode="values"
# ):
#     event["messages"][-1].pretty_print()
