from agents06 import Analyzer_agent, Critic_agent, Database_agent
from langgraph.graph import StateGraph, START, END
from state06 import State
from typing import Literal

def router(state: State) -> Literal["__end__", "Critic", "Analyst","Database"]:
    if state["next"] == "Critic":
        return "Critic"
    elif state["next"] == "Database":
        return "Database"
    elif state["next"] == "END":
        return "__end__"
    else:
        return "Analyst"
builder = StateGraph(State)
builder.add_node("Critic", Critic_agent)
builder.add_node("Database", Database_agent)
builder.add_node("Analyzer", Analyzer_agent)
builder.add_edge(START, "Analyzer")
builder.add_conditional_edges("Analyzer", router)
builder.add_conditional_edges("Critic", router)
builder.add_conditional_edges("Database", router)

graph = builder.compile(interrupt_before=["Critic","Database"])
