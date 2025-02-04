from langchain_groq import ChatGroq
from langchain_community.utilities.sql_database import SQLDatabase
from langgraph.graph import START, END, StateGraph

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)