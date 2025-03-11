from langgraph.graph import START, END, StateGraph
from langgraph_swarm.swarm import StateGraph as SwarmStateGraph,
from langgraph.prebuilt import tools_condition,ToolNode
from Nodes10 import internet, math
from tools10 import add,divide,factorial,multiply,power,subtract,sqrt,tavily,to_internet,to_math
from state10 import State

internet_builder = StateGraph(State)
internet_builder.add_node("Internet", internet)
internet_builder.add_node("tools",ToolNode([tavily,to_math]))
internet_builder.add_edge(START, "Internet")
internet_builder.add_conditional_edges("Internet", tools_condition)
internet_builder.add_edge("tools", "Internet")
internet_builder.add_edge("Internet", END)

internet_graph=internet_builder.compile(interrupt_before=["tools"]) 

math_builder = StateGraph(State)
math_builder.add_node("math", math)
math_builder.add_node("tools",ToolNode([multiply, divide, add, subtract, power, sqrt, factorial,to_internet]))
math_builder.add_edge(START, "math")
math_builder.add_conditional_edges("math", tools_condition)
math_builder.add_edge("tools", "math")
math_builder.add_edge("math", END)

math_graph = math_builder.compile(interrupt_before=["tools"])
