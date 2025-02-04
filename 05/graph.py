from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import Engine, create_engine
from langgraph.graph import StateGraph, START, END,MessagesState

class 
    
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

