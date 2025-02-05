from typing import Literal
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode
from tools import  tool
from state import State

from agents import CEO_agent,Internet_agent,Planner_agent

def router(state:State)->Literal["CEO","Internet","Planner"]:
    if state["next"] == "Internet":
        return "Internet"
    elif state["next"] == "Planner":
        return "Planner"
    else :
        return "CEO"

builder =StateGraph(State)
builder.add_node("CEO",CEO_agent)
builder.add_node("Planner",Planner_agent)
builder.add_node("Internet",Internet_agent)
builder.add_node("tools",ToolNode([tool]))


