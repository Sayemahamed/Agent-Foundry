from typing import TypedDict, Annotated, Optional


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*options]
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next: Optional[str]