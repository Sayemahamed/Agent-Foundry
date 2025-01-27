from typing import Literal, TypedDict, Annotated, Optional
from langgraph.graph import START, END, StateGraph
from langchain_ollama import ChatOllama
from langgraph.graph.message import BaseMessage, add_messages
from langchain_core.messages import  HumanMessage


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: Optional[str]


agent = ChatOllama(
    model="granite3.1-moe",
    temperature=0.9,
)


def decider(state: State) -> Literal["agent", "summarize"]:
    if len(state["messages"]) >= 5:
        return "summarize"
    else:
        return "agent"


def call_agent(state: State) -> State:
    summary = state.get("summary", "")
    agent_response = agent.invoke(state["messages"])
    updated_messages = state["messages"] + [agent_response]
    return {"messages": updated_messages, "summary": summary}


def summarize(state: State) -> State:
    previous_summary: str = state.get("summary", "")  # type: ignore
    summary = agent.invoke(
        state["messages"][:4]
        + [
            HumanMessage(
                content="""Summarize the conversation between the user and the AI assistant.
Cluster related ideas to condense the information.
Eliminate repetition from the summary."""
            ),
        ]
    ).content
    if len(previous_summary) > 0:
        summary = agent.invoke(
            [
                HumanMessage(
                    content=f"""
Merge the summary and keep key points.

Previous summary: {previous_summary}

New summary: {summary}
"""
                )
            ]
        ).content
    # Remove the first 4 messages (excluding the last 2)
    updated_messages = state["messages"][-2:]
    return {"summary": summary, "messages": updated_messages}


builder = StateGraph(State)

builder.add_node("agent", call_agent)
builder.add_node("summarize", summarize)

builder.add_conditional_edges(START, decider)
builder.add_edge("summarize", "agent")
builder.add_edge("agent", END)

graph = builder.compile()