from random import choice
from pydantic import BaseModel
from typing import Optional

class State(BaseModel):
    initialS:Optional[str]=None
    intermediateS:Optional[str]=None
    finalS:Optional[str]=None