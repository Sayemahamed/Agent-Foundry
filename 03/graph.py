from langgraph.graph import START, END, StateGraph
from state03 import State
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from tools03 import *
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

memory = MemorySaver()

# agent = ChatOllama(
#     model="qwen2.5:0.5b",
#     # model="granite3.1-moe",
#     temperature=0,
# )
agent = ChatGroq(model="llama3-8b-8192", temperature=0.7)
agent = agent.bind_tools([multiply, divide, add, subtract, pow, sqrt, factorial])


def call_agent(state: State):
    temp = agent.invoke(state["messages"])
    print(temp)
    return {"messages": temp}


builder = StateGraph(State)

builder.add_node("agent", call_agent)
builder.add_node(
    "tools", ToolNode([multiply, divide, add, subtract, pow, sqrt, factorial])
)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.add_edge("agent", END)

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
