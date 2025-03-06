from typing import Literal
from langgraph.graph import MessagesState
from pydantic import BaseModel


class AgentResponse(BaseModel):
    Message: str
    Next: Literal[ "Critic", "Database", "END"]


class State(MessagesState):
    criticized: int
    pre: Literal["Critic", "Database"]
