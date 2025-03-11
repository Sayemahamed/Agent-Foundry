from state10 import State
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(name="gpt-4o-mini", temperature=0)

def sayem(state:State):