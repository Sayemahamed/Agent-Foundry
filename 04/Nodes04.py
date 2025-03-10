from langchain_openai import ChatOpenAI
from state04 import State
from typing import Literal
from langchain_core.messages import HumanMessage


agent = ChatOpenAI(name="gpt-4o-mini", temperature=0)


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
        "summary": summary,  # type: ignore
        "messages": [RemoveMessage(x.id) for x in state["messages"][:-1]],  # type: ignore
    }
