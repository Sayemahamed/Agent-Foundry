from typing import Literal, TypedDict, Annotated, Optional
from langgraph.graph import START, END, StateGraph
from langchain_ollama import ChatOllama
from langgraph.graph.message import BaseMessage, add_messages, RemoveMessage
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: Optional[str]


agent = ChatOllama(
    model="qwen2.5:0.5b",
    # model="granite3.1-moe",
    temperature=0.9,
)
# agent = ChatGroq(model="llama3-8b-8192", temperature=0.7)


def decider(state: State) -> Literal["agent", "summarize"]:
    print("^" * 60)
    print(len(state["messages"]))
    print("^" * 60)
    if len(state["messages"]) >= 5:
        return "summarize"
    else:
        return "agent"


def call_agent(state: State) -> State:
    # print("^" * 60)
    # for message in state["messages"]:
    #     message.pretty_print()
    summary = state.get("summary", "")
    if not summary:
        summary = ""
    if len(summary) > 0:
        print("*" * 100)
        print("Previous summary detected in Agent Node ")
        print("*" * 100)
        agent_response = agent.invoke(
            [HumanMessage(content="Previous conversation summary: " + summary)]
            + state["messages"]
        )
    else:
        agent_response = agent.invoke(state["messages"])
    return {"messages": [agent_response], "summary": summary}


def summarize(state: State) -> State:
    # print("*" * 60)
    # for message in state["messages"]:
    #     message.pretty_print()
    #     print(message.id)
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
        print("*" * 100)
        print("Previous summary detected in Summary Node ")
        print("*" * 100)
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
    return {
        "summary": summary, # type: ignore
        "messages": [RemoveMessage(x.id) for x in state["messages"][:-1]], # type: ignore
    }


builder = StateGraph(State)

builder.add_node("agent", call_agent)
builder.add_node("summarize", summarize)

builder.add_conditional_edges(START, decider)
builder.add_edge("summarize", "agent")
builder.add_edge("agent", END)

graph = builder.compile(checkpointer=MemorySaver())

# graph.invoke(
#     {"messages": [HumanMessage(content="Hello, I am Sayem")]},
#     {"configurable": {"thread_id": 1}},
# )
# graph.invoke(
#     {"messages": [HumanMessage(content="can You Help me with maths")]},
#     {"configurable": {"thread_id": 1}},
# )
graph.invoke(
    {"messages": [HumanMessage(content="who are You?")]},
    {"configurable": {"thread_id": 1}},
)
