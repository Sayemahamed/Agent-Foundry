from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode,tools_condition
from state import State
from agents import CEO_agent, Critic_agent, Planner_agent

def router(state: State) -> Literal["CEO", "Critic", "Planner"]:
    print(state)
    print("---router---")
    # Route based on the 'next' field in the state
    if state["next"] == "Critic":
        return "Critic"
    elif state["next"] == "Planner":
        return "Planner"
    else:
        return "CEO"

# Build the state graph with defined nodes and transitions
builder = StateGraph(State)
builder.add_node("CEO", CEO_agent)
builder.add_node("Planner", Planner_agent)
builder.add_node("Critic", Critic_agent)
builder.add_edge(START, "CEO")
builder.add_conditional_edges("CEO", router)
builder.add_conditional_edges("Planner", router)
builder.add_conditional_edges("Critic", router)
builder.add_edge("tools", "Internet")
builder.add_edge("CEO", END)

graph = builder.compile(interrupt_before=["tools","CEO","Internet","Planner"])
