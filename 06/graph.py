from agents06 import Analyzer_agent, Critic_agent, Database_agent
from langgraph.graph import StateGraph, START, END
from state06 import State


builder = StateGraph(State)
builder.add_node("Critic", Critic_agent)
builder.add_node("Database", Database_agent)
builder.add_node("Analyst", Analyzer_agent)
builder.add_edge(START, "Analyst")
builder.add_edge("Analyst", END)

graph = builder.compile(interrupt_before=["Critic","Database"])
