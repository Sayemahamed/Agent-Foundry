from pydantic import BaseModel
from typing import Literal
from langgraph.graph.message import MessagesState


class AgentOutput(BaseModel):
    message: str
    next: Literal["User", "Job", "Critic", "Industry", "END", "Coach"]


class State(MessagesState):
    criticizes: int
    pre:Literal["User", "Job", "Critic", "Industry"]
