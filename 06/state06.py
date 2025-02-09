from typing import Literal
from langgraph.graph import MessagesState
from pydantic import BaseModel

class AgentResponse(BaseModel):
    message:str
    next:Literal["Planner", "Critic", "Database"]

class State(MessagesState):
    criticized:int
    next:str
