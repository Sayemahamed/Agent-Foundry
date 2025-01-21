from langgraph.graph import START,END,StateGraph,MessagesState
# from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from IPython.display import Image, display
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver,PersistentDict

class MessageState(MessagesState):
    summary:str
memory = MemorySaver()
agent = ChatOllama(
    model="granite3.1-moe", temperature=0.7
)
# agent = ChatGroq(model="llama3-8b-8192", temperature=0.7)
def invoke(state: MessageState):
    conversation_summary =state.get("summary","")
    return {"messages": [agent.invoke(state["messages"])], "summary":conversation_summary}

def summarize(state: MessageState):
    internal_message=[
        SystemMessage(content="""Analyze the conversation between the user and the AI assistant.
Identify and extract new key points.
Cluster related ideas to condense the information.
Eliminate repetition from the conversation and the previous summary.
Update the summary only when new information is present."""),
        SystemMessage(content="Previous summary: "+state["summary"])
    ]+state["messages"]
    for message in internal_message:
        message.pretty_print()
    response=agent.invoke(internal_message)
    return {"summary":response.content}

builder = StateGraph(MessageState)

builder.add_node("agent", invoke)
builder.add_node("summarizer", summarize)

builder.add_edge(START, "agent")
builder.add_edge("agent", "summarizer")
builder.add_edge("summarizer", END)

graph = builder.compile(checkpointer=memory)

display(Image(graph.get_graph().draw_mermaid_png()))

message = [
    HumanMessage(content="Which nation has the highest life expectancy?"),
]
config: dict[str, dict[str, str]] = {"configurable": {"thread_id": "1"}}
response=graph.invoke({"messages": message}, config=config) # type: ignore

for message in response["messages"]:
    message.pretty_print()

print("*"*90)
print(response["summary"])