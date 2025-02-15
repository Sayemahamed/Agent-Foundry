from langchain_openai import ChatOpenAI
from state06 import AgentResponse
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import json

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def invoke_llm(prompt: list[BaseMessage]) -> AgentResponse:
    response: AIMessage = llm.invoke(prompt)  # type: ignore

    try:
        response_json = json.loads(str(response.content))
        return AgentResponse.model_validate(response_json)  
    except Exception as e:
        print(f"Error parsing response: {e}")  
        validation_schema = json.dumps(AgentResponse.model_json_schema(), indent=2)
        return invoke_llm([
            AIMessage(content=response.content),
            HumanMessage(content=f"Provide a valid JSON response that matches this schema:\n{validation_schema}")
        ])

if __name__ == "__main__":
    print(invoke_llm([HumanMessage(content="What is the best next step after analyzing user data?")]))