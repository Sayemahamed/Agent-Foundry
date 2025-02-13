from typing import Literal
from langgraph.graph import MessagesState
from pydantic import BaseModel

class AgentResponse(BaseModel):
    message:str
    next:Literal["Analyst", "Critic", "Database","END"]

class State(MessagesState):
    criticized:int
    pre:Literal["Analyst", "Critic", "Database"]
