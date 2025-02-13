from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class AgentOutput(BaseModel):
    message: str
    next: str

llm = ChatOpenAI(model="gpt-4o-mini")

llm=llm.with_structured_output(schema=AgentOutput)