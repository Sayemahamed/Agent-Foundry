from tempfile import tempdir
from typing import TypedDict, Annotated, Optional
from langgraph.graph import START, END, StateGraph
from langchain_ollama import ChatOllama
from langgraph.graph.message import BaseMessage, add_messages, RemoveMessage
from langchain_core.messages import SystemMessage


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: Optional[str]


agent = ChatOllama(
    # model="qwen2.5:0.5b",
    model="granite3.1-moe",
    temperature=0.9,
)


def call_agent(state: State) -> State:
    summary = state.get("summary", "")
    return {"messages": [agent.invoke(state["messages"])], "summary": summary}


def summarize(state: State) -> State:
    summary: str = state.get("summary", "No Summary")  # type: ignore
    print(summary)
    print("=" * 80)
    temp = agent.invoke(
        state["messages"]
        + [
            SystemMessage(content="Previous Summary: " + summary),
            SystemMessage(
                content="""Summarize the conversation between the user and the AI assistant.
Cluster related ideas to condense the information.
Eliminate repetition from the summary.
Update the summary only when new information is present.
"""
            ),
        ]
    )
    print(temp)
    return {"summary": temp.content}  # type: ignore


builder = StateGraph(State)

builder.add_node("agent", call_agent)
builder.add_node("summarize", summarize)

builder.add_edge(START, "agent")
builder.add_edge("agent", "summarize")
builder.add_edge("summarize", END)

graph = builder.compile()
