from langgraph.graph import START, END, StateGraph, MessagesState
from langchain_ollama import ChatOllama
from IPython.display import Image, display
from langchain_core.messages import SystemMessage, HumanMessage, AnyMessage
from typing import Dict, List


class MessagesState(MessagesState):
    pass


agent = ChatOllama(
    model="hf.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF",
    temperature=0.7,
)


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


agent = agent.bind_tools([multiply])


def invoke(state: MessagesState) -> Dict[str, List]:
    """Process the current state through the agent.

    Args:
        state (MessagesState): Current state containing message history

    Returns:
        Dict[str, List]: Updated state with new messages
    """
    return {"messages": [agent.invoke(state["messages"])]}


builder = StateGraph(MessagesState)

builder.add_node("agent", invoke)
builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

message = [
    SystemMessage(
        content="You are Qwen, a math problem solver. You will be given a math problem and your task is to solve it using the tools provided."
    ),
    HumanMessage(content="What is 2 * 3?"),
    HumanMessage(content="What is 4 * 5?"),
    HumanMessage(content="What is 6 * 7?"),
]

for message in graph.invoke({"messages": message})["messages"]:
    message.pretty_print()
