from pydantic import BaseModel
from typing import Optional

class State(BaseModel):
    initialS:Optional[str]
    intermediateS:Optional[str]
    finalS:Optional[str]