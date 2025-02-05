from langchain_groq import ChatGroq
from state import State, AgentOutput
from langchain_core.messages import SystemMessage, AIMessage

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)


def CEO_agent(state: State) -> State:
    print("---CEO_agent---")
    response = llm.with_structured_output(schema=AgentOutput).invoke(
        [
            SystemMessage(
                content="""## Role: CEO of a Research Team  

You are the **CEO** of a research team that includes:  
- A **Planner** responsible for structuring the research process.  
- An **Internet Researcher** who gathers relevant information.  
- **You**, the leader who coordinates the team and ensures high-quality research.  

### Task:  
Your objective is to **collaborate** with your team members to **conduct thorough research** on the given topic.  
- **Delegate tasks effectively.**  
- **Ensure accuracy and depth** in the research.  
- **Synthesize information** into a structured and insightful report.  

Leverage your team’s strengths to **produce well-organized and insightful research** on the topic provided.  
"""
            ),
        ]
        + state["messages"]
    )
    return {"messages": [AIMessage(content=response.message)], "next": response.next}

def Planner_agent(state: State) -> State:
    print("---Planner_agent---")
    response = llm.with_structured_output(schema=AgentOutput).invoke(
        [           SystemMessage(
                content="""## Role: Planner of a Research Team  

You are the **Planner** of a research team that includes:  
- An **Internet Researcher** who gathers relevant information.  
- **You**, the leader who coordinates the team and ensures high-quality research.  

### Task:   
Your objective is to **collaborate** with your team members to **conduct thorough research** on the given topic.  
- **Delegate tasks effectively.**   
- **Ensure accuracy and depth** in the research.  
- **Synthesize information** into a structured and insightful report.  

Leverage your team’s strengths to **produce well-organized and insightful research** on the topic provided.  
"""
            )+state["messages"]])
    return {"messages": [AIMessage(content=response.message)], "next": response.next}

def Internet_agent(state:State)->State:
    