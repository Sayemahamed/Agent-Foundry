from typing import TypedDict, Annotated, Optional, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages,MessagesState
from pydantic import BaseModel

class AgentOutput(BaseModel):
    message: str
    next: Literal["Planner", "Critic", "CEO"]

class State(MessagesState):
    next: Optional[str]
