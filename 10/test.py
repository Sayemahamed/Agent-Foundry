from typing_extensions import TypedDict, Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import StateGraph, add_messages
from langgraph_swarm import SwarmState

class AliceState(TypedDict):
    alice_messages: Annotated[list[AnyMessage], add_messages]

# see this guide to learn how you can implement a custom tool-calling agent
# https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/
alice = (
    StateGraph(AliceState)
    .add_node("model", ...)
    .add_node("tools", ...)
    .add_edge(...)
    ...
    .compile()
)

# wrapper calling the agent
def call_alice(state: SwarmState):
    # you can put any input transformation from parent state -> agent state
    # for example, you can invoke "alice" with "task_description" populated by the LLM
    response = alice.invoke({"alice_messages": state["messages"]})
    # you can put any output transformation from agent state -> parent state
    return {"messages": response["alice_messages"]}

def call_bob(state: SwarmState):
    ...

from langgraph_swarm import add_active_agent_router

workflow = (
    StateGraph(SwarmState)
    .add_node("Alice", call_alice, destinations=("Bob",))
    .add_node("Bob", call_bob, destinations=("Alice",))
)
# this is the router that enables us to keep track of the last active agent
workflow = add_active_agent_router(
    builder=workflow,
    route_to=["Alice", "Bob"],
    default_active_agent="Alice",
)

# compile the workflow
app = workflow.compile()