from langchain_core.messages.ai import AIMessage, AIMessageChunk
from langchain_core.messages.chat import ChatMessage, ChatMessageChunk
from langchain_core.messages.function import FunctionMessage, FunctionMessageChunk
from langchain_core.messages.human import HumanMessageChunk
from langchain_core.messages.system import SystemMessageChunk
from langchain_core.messages.tool import ToolMessage, ToolMessageChunk
from langgraph.graph import START, END, StateGraph,MessagesState
from langchain_ollama import ChatOllama
from IPython.display import Image, display
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph

class MessageState(MessagesState):
    previous_summary: str

memory = MemorySaver()

agent = ChatOllama(
    model="granite3.1-moe", temperature=0.7
)

def invoke(state: MessageState):
    previous_summary: str = state.get("previous_summary","")
    return {"messages":[agent.invoke(input=state["messages"])],"previous_summary":previous_summary}

def summarize(state:MessageState):
    internal_message: list[AIMessage | HumanMessage | ChatMessage | SystemMessage | FunctionMessage | ToolMessage | AIMessageChunk | HumanMessageChunk | ChatMessageChunk | SystemMessageChunk | FunctionMessageChunk | ToolMessageChunk]=[
        SystemMessage(content="""Analyze the conversation between the user and the AI assistant.
Identify and extract new key points.
Cluster related ideas to condense the information.
Eliminate repetition from the conversation and the previous summary.
Update the summary only when new information is present.
"""),
SystemMessage("Previous Summary: "+state["previous_summary"])]+state["messages"]
    return {"summary":agent.invoke(input=internal_message).content}

builder = StateGraph(MessageState)
builder.add_node(node="agent", action=invoke)
builder.add_node(node="summarizer",action=summarize)

builder.add_edge(start_key=START,end_key="agent")
builder.add_edge(start_key="agent", end_key="summarizer")
builder.add_edge(start_key="summarizer",end_key=END)

graph: CompiledStateGraph = builder.compile(checkpointer=memory)

display(Image(graph.get_graph().draw_mermaid_png()))

config ={"configurable": {"thread_id": "1"}}

response=graph.invoke({"messages":[HumanMessage("who are you")]},config=config) # type: ignore

for message in response["messages"]:
    message.pretty_print()

print("*"*90)
print(response["previous_summary"])