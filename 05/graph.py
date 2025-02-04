from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import Engine, create_engine
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.graph import StateGraph, START, END, MessagesState

class State(MessagesState):
    pass
    
# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=1)

# Correct Database Connection
engine: Engine = create_engine("sqlite:///database.sqlite")  # Connects to your actual SQLite file
db = SQLDatabase(engine=engine)

# Create SQL Agent
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",  # or "zero-shot-react-description" depending on your preference
    verbose=True  # Enable for debugging
)

# ✅ FIX: Ensure the correct input format is passed to agent_executor.run()
def call_agent(state: State) -> State:
    input_text = state["messages"][-1].content  # Extract the last message content
    response = agent_executor.run({"input": input_text})  # Pass as dictionary with "input" key
    print(response)
    return {"messages": [AIMessage( response)]}  # Ensure the output format matches expected structure

# ✅ FIX: Ensure the state machine passes the correct input format
builder = StateGraph(state_schema=State)

builder.add_node(node="agent", action=call_agent)  # Call `call_agent()` instead of `agent_executor.run`
builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile()
