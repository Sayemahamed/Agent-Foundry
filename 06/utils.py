from langchain_openai import ChatOpenAI
from state06 import AgentResponse
from langchain_core.messages.base import BaseMessage
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def invoke_llm(prompt: list[BaseMessage]) -> AgentResponse:
    response: BaseMessage = llm.invoke(prompt)
    try:
        return AgentResponse.model_validate_json(str(response.content))
    except:
        return invoke_llm([HumanMessage(content="Give valid JSON response"),AIMessage(content=str(response.content))])
