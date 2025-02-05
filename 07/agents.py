from langchain_groq import ChatGroq
from state import State, AgentOutput
from langchain_core.messages import SystemMessage, AIMessage
from tools import tool

# Initialize the LLM with the desired model and temperature
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

def CEO_agent(state: State) -> State:
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
    print (response)
    return {"messages": [AIMessage(content=response.message)], "next": response.next}

def Planner_agent(state: State) -> State:
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
    print (response)
    return {"messages": [AIMessage(content=response.message)], "next": response.next}

# Bind tools to the LLM if needed (e.g., for internet searches)
llm = llm.bind_tools([tool])

def Internet_agent(state: State) -> State:
    print("------Internet_agent--------")
    response = llm.with_structured_output(schema=AgentOutput).invoke(
        [
            SystemMessage(
                content="""\
## Role: Internet Researcher of a Research Team

You are the **Internet Researcher** tasked with gathering data and information from online sources.
- You work under the guidance of the CEO and Planner.
- Your findings will support the overall research report.

### Task:
Search the internet for relevant information on the given topic.
- **Identify credible sources** and extract key data.
- **Summarize your findings** concisely.
- **Provide references** where applicable.

Deliver detailed, verified information that can be integrated into the final report.
"""
            )
        ] + state["messages"]
    )
    print (response)
    return {"messages": [AIMessage(content=response.message)], "next": response.next}
