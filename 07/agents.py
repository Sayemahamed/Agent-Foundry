from langchain_groq import ChatGroq
from state import State
from langchain_core.messages import SystemMessage
from langgraph.types import Command

llm = ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)

def CEO_agent(state: State):
    print("---CEO_agent---")
    return {""}