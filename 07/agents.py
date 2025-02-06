from langchain_groq import ChatGroq
from state import State, AgentOutput
from langchain_core.messages import SystemMessage, AIMessage
# Import our tool functions from the tools module
from tools import  tavily_tool, duck_tool, wikipedia_tool

# Initialize the LLM with the desired model and temperature
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

def CEO_agent(state: State) -> State:
    """
    CEO Agent: Coordinates the research team, delegates tasks, and synthesizes inputs.
    """
    print("---CEO_agent---")
    response = llm.with_structured_output(schema=AgentOutput).invoke(
        [
            SystemMessage(
                content="""\
## Role: CEO of a Research Team

You are the **CEO** of a research team that includes:
- A **Planner** responsible for structuring the research process.
- An **Internet Researcher** who gathers relevant information.
- **You**, the leader who coordinates the team and ensures high-quality research.

### Task:
Collaborate with your team members to conduct thorough research on the given topic.
- **Delegate tasks effectively.**
- **Ensure accuracy and depth** in the research.
- **Synthesize information** into a structured, insightful report.

Leverage your team’s strengths to produce well-organized and insightful research on the provided topic.
"""
            )
        ] + state["messages"]
    )
    print("CEO_agent response:", response)
    return {"messages": [AIMessage(content=response.message)], "next": response.next}

def Planner_agent(state: State) -> State:
    """
    Planner Agent: Designs a research plan, outlines steps, and allocates tasks.
    """
    print("---Planner_agent---")
    response = llm.with_structured_output(schema=AgentOutput).invoke(
        [
            SystemMessage(
                content="""\
## Role: Planner of a Research Team

You are the **Planner** for a research team that includes:
- An **Internet Researcher** who gathers relevant information.
- A **CEO** who leads and coordinates the research effort.

### Task:
Design a clear and efficient research plan for the given topic.
- **Outline the research process step-by-step.**
- **Identify key areas** that require further investigation.
- **Allocate tasks** to team members effectively.

Provide a detailed plan to ensure comprehensive coverage of the topic.
"""
            )
        ] + state["messages"]
    )
    print("Planner_agent response:", response)
    return {"messages": [AIMessage(content=response.message)], "next": response.next}

def Critic_agent(state: State) -> State:
    """
    Critic Agent: Reviews the research report and provides feedback.
    """
    print("---Critic_agent---")
    response = llm.with_structured_output(schema=AgentOutput).invoke(
        [
            SystemMessage(
                content="""\
## Role: Research Critic of a Research Team

You are the **Critic** for a research team that includes:
- A **Planner** who designs the research plan.
- An **Internet Researcher** who gathers relevant information.
- A **CEO** who leads and coordinates the research effort.

### Task:   
Review the research report and provide constructive feedback.
- **Identify areas for improvement.**
- **Suggest alternative approaches.**
- **Evaluate the accuracy and depth of the report.**

Provide constructive feedback to improve the research report.
"""
            )    
        ] + state["messages"]
    )
    print("Critic_agent response:", response)
    return {"messages": [AIMessage(content=response.message)], "next": response.next}