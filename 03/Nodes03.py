from langchain_openai import ChatOpenAI
from state03 import State
from tools03 import *

agent = ChatOpenAI(name="gpt-4o-mini", temperature=0)
agent = agent.bind_tools(
    tools=[multiply, divide, add, subtract, power, sqrt, factorial]
)


def call_agent(state: State):
    temp = agent.invoke(state["messages"])
    print(temp)
    return {"messages": temp}
