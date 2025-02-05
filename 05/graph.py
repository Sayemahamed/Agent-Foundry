from langchain_core.messages.base import BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph,MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

class State(MessagesState):
    pass

connection = sqlite3.connect("db.sqlite")
con =sqlite3.connect("database.sqlite").cursor()
memory = SqliteSaver(conn=connection)


llm = ChatGroq(model="llama3-8b-8192", temperature=0.7)

def database(str: str) :
    """
    Executes a SQL query on the connected SQLite database and retrieves all results.

    Parameters:
        str (str): The SQL query to execute.

    Returns:
        list: A list of tuples containing the results of the query.
    """
    print(str)
    return con.execute(str).fetchall()

llm = llm.bind_tools([database])
def agent(state: State):
    temp = llm.invoke(state["messages"])
    print(temp)
    return {"messages": temp}


builder = StateGraph(State)

builder.add_node("agent", agent)
builder.add_node("tools",ToolNode([database]))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.add_edge("agent", END)

graph: CompiledStateGraph = builder.compile(interrupt_before=["tools"],checkpointer=memory)