from pydantic import BaseModel, field_validator
from langchain_core.messages import AnyMessage

class State(BaseModel):
    messages: list[AnyMessage]

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v):
        # You can add custom validation logic here
        return v