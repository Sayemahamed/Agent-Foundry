from langgraph.graph import START, END,StateGraph
from state import State
from langchain_ollama import ChatOllama


agent = ChatOllama(
    model="qwen2.5:0.5b",
    # model="granite3.1-moe",
    temperature=0.9,
)

def call_agent(state: State) -> State:
    temp=agent.invoke(state.messages)
    print(temp)
    state.messages.append(temp) # type: ignore
    return state


builder = StateGraph(State)

builder.add_node("agent", call_agent)

builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile()