from typing import TypedDict, Annotated, Optional, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel


class AgentOutput(BaseModel):
    message: str
    next: Literal["researcher", "internet_researcher"]


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next: Optional[str]
