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

def Internet_agent(state: State) -> State:
    """
    Internet Agent: Searches for relevant data online using the LLM and bound tools.
    """
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
    print("Internet_agent response:", response)
    return {"messages": [AIMessage(content=response.message)], "next": response.next}

def Search_agent(state: State) -> State:
    """
    Search Agent: Uses multiple external search tools to gather diverse information
    on the research topic, and then synthesizes these findings into a summary.
    """
    print("-----Search_agent-----")
    # Assume that the latest message holds the research topic/query.
    if state["messages"]:
        query = state["messages"][-1].content
    else:
        query = "default topic"
    
    # Get search results from multiple tools.
    print("Searching for topic:", query)
    tavily_result = tavily_tool(query)
    wiki_result = wikipedia_tool(query)
    duck_result = duck_tool(query)
    
    # Combine results into one summary prompt.
    combined_results = (
        f"### Search Results for: {query}\n\n"
        f"**Tavily Search:**\n{tavily_result}\n\n"
        f"**Wikipedia Summary:**\n{wiki_result}\n\n"
        f"**DuckDuckGo Search:**\n{duck_result}"
    )
    print("Combined search results:\n", combined_results)
    
    # Use the LLM to synthesize the combined search results.
    response = llm.with_structured_output(schema=AgentOutput).invoke(
        [
            SystemMessage(
                content="""\
## Role: Search Synthesizer

You are tasked with synthesizing multiple search results into a coherent summary.
### Task:
Combine the provided search results into a concise and informative summary that highlights key insights and data points.
"""
            ),
            SystemMessage(content=combined_results)
        ] + state["messages"]
    )
    print("Search_agent response:", response)
    return {"messages": [AIMessage(content=response.message)], "next": response.next}

# Bind the primary tool to the LLM (this could be used as a fallback or for simple queries)
llm = llm.bind_tools([tavily_tool])
