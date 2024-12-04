from langchain_ollama import ChatOllama
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage
from IPython.display import Image, display
from typing import Dict, List
from langgraph.prebuilt import ToolNode, tools_condition
import math
from langgraph.checkpoint.memory import MemorySaver
# from langchain_groq import ChatGroq

memory = MemorySaver()


class MessagesState(MessagesState):
    pass


def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Parameters:
        a (float): First number to multiply
        b (float): Second number to multiply

    Returns:
        float: The product of the two numbers
    """
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers.

    Parameters:
        a (float): First number to add
        b (float): Second number to add

    Returns:
        float: The sum of the two numbers
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract two numbers.

    Parameters:
        a (float): First number to subtract
        b (float): Second number to subtract

    Returns:
        float: The difference of the two numbers
    """
    return a - b


def divide(a: float, b: float) -> float:
    """Divide two numbers.

    Parameters:
        a (float): First number to divide
        b (float): Second number to divide

    Returns:
        float: The quotient of the two numbers
    """
    return a / b


def power(base: float, exponent: float) -> float:
    """Calculate base raised to exponent.

    Parameters:
        base (float): The base number
        exponent (float): The exponent to raise the base to

    Returns:
        float: The result of base raised to the power of exponent
    """
    return base**exponent


def sqrt(value: float) -> float:
    """Calculate the square root of a number.

    Parameters:
        value (float): The number to calculate the square root of

    Returns:
        float: The square root of the number
    """
    return math.sqrt(value)


def factorial(n: int) -> int | None:
    """Calculate the factorial of a number.

    Parameters:
        n (int): The number to calculate the factorial of

    Returns:
        int: The factorial of the number
    """
    return math.factorial(n) if n >= 0 else None


def call_agent(state: MessagesState) -> Dict[str, List]:
    """Process the current state through the agent.

    Args:
        state (MessagesState): Current state containing message history

    Returns:
        Dict[str, List]: Updated state with new messages
    """
    return {"messages": [agent.invoke(state["messages"])]}


# Configure the agent with specific parameters
agent = ChatOllama(
    model="hf.co/Qwen/Qwen2.5-3B-Instruct-GGUF",
    temperature=0.7,
)
# agent = ChatGroq(model="llama3-8b-8192", temperature=0.7)
agent = agent.bind_tools([multiply, add, subtract, divide, power, sqrt, factorial])

# Build the graph
builder = StateGraph(MessagesState)
builder.add_node("agent", call_agent)
builder.add_node(
    "tools", ToolNode([multiply, add, subtract, divide, power, sqrt, factorial])
)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
# builder.add_edge("agent", END)
builder.add_edge("tools", "agent")

graph = builder.compile(checkpointer=memory)

# Initial messages
message = [
    SystemMessage(
        content="""You are Qwen, a math problem solver. 
        You will be given a math problem and your task is to solve it using the tools provided.
        For complex query solve it by dividing the problem into sub problems and solve one at a time.
        Available tools:
        - add(a, b): Add two numbers
        - subtract(a, b): Subtract two numbers
        - multiply(a, b): Multiply two numbers
        - divide(a, b): Divide two numbers
        - power(base, exponent): Calculate base raised to exponent
        - sqrt(x): Calculate square root
        - abs(x): Calculate absolute value
        - factorial(n): Calculate factorial
        """
    ),
    HumanMessage(content="what is 69 / 3 + 3 - 3 * 1 ?"),
]

# Visualize the graph
display(Image(graph.get_graph().draw_mermaid_png()))
config = {"configurable": {"thread_id": "1"}}
# message = [HumanMessage("now subtract 19")]
try:
    # Process messages through the graph
    result = graph.invoke({"messages": message}, config=config)
    for message in result["messages"]:
        message.pretty_print()
except Exception as e:
    print(f"Error processing messages: {str(e)}")
