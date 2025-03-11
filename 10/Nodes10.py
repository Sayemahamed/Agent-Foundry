from state10 import State
from langchain_openai import ChatOpenAI
from tools10 import add,divide,factorial,multiply,power,subtract,sqrt,tavily,to_internet,to_math
from langchain_core.messages import SystemMessage


llm = ChatOpenAI(name="gpt-4o-mini", temperature=0)

internet_llm = llm.bind_tools(tools=[tavily,to_math])

math_llm = llm.bind_tools(tools=[multiply, divide, add, subtract, power, sqrt, factorial,
    to_internet])

def math(state:State):
    return {"messages":math_llm.invoke(state["messages"]+[SystemMessage(content="You are a math expert")])}

def internet(state:State):
    return {"messages":internet_llm.invoke(state["messages"]+[SystemMessage(content="You are a web expert")])}