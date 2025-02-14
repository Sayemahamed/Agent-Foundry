from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from rich import print


class AgentOutput(BaseModel):
    message: str
    next_step: str


parser = PydanticOutputParser(pydantic_object=AgentOutput)

prompt = PromptTemplate(
    template="You are an AI agent. Based on the following input, generate a structured response:\n\n{input}\n\n{format_instructions}",
    input_variables=["input"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

prompt

llm = ChatOpenAI(model="gpt-4o-mini")

temp =prompt.format(input="What is the best next step after analyzing user data?")
print(temp)

response = llm.invoke(
    prompt.format(input="What is the best next step after analyzing user data?")
)
response
parsed_response = parser.parse(text=str(response.content))

print(parsed_response)
parsed_response.next_step
parsed_response.message
