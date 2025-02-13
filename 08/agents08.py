from langgraph.types import Command, interrupt
from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from state08 import State, AgentOutput
from rich import print
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(schema=AgentOutput)
coach_prompt:str="""
Coach
"""
critic_prompt:str="""
Critic
"""

def User_interface(state: State) -> Command[Literal["Coach"]]:
    print("---User_interface---")
    user_action = interrupt(value=state["messages"][-1].content)
    return Command(
        update={"messages": [HumanMessage(content=user_action)]}, goto="Coach"
    )

def Coach_agent(state:State)->Command[Literal["User", "Job", "Critic", "Industry", "END"]]:
    print("---Coach_agent---")
    if state["criticizes"]<2:
        response=llm.invoke([SystemMessage(content=coach_prompt)]+state["messages"])
    else:
        response=llm.invoke([SystemMessage(content=coach_prompt)]+state["messages"]+[HumanMessage(content="Finalize and conclude the process and deliver the report.")])
    return Command(
        update={"messages": [AIMessage(content=response.message)],"pre":"Coach"}, goto=response.next if response.next!="END" else "__end__"
    )

def Critic_agent(state:State)->Command[Literal["Job", "Coach", "Industry"]]:
    print("---Critic_agent---")
    response=llm.with_structured_output(schema=AgentOutput).invoke([SystemMessage(content=critic_prompt)]+state["messages"])
    return Command(
        update={"messages": [AIMessage(content=response.message)],"criticizes":state["criticizes"]+1,"pre":"Critic"}, goto=response.next
    )

def Job_lister(state:State)->Command[Literal["Critic", "Coach"]]:
    print("---Job_lister---")
    tavily = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
    # include_domains=[...],
    # exclude_domains=[...],
    # name="...",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
    )
    loader = FireCrawlLoader(
    api_key="YOUR_API_KEY",
    url="https://firecrawl.dev",
    mode="crawl",
)