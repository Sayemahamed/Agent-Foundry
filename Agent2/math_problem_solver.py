from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.tools import tool
import math

# Initialize the agent
agent = ChatOllama(model="hf.co/Qwen/Qwen2.5-3B-Instruct-GGUF", temperature=0.7)

# System message defining the agent's role
messages: list[BaseMessage] = [
    SystemMessage(
        content="""
        You are Qwen, a math problem solver. You will be given a math problem and your task is to solve it using the tools provided.
        Available tools:
        - add(a, b): Add two numbers
        - subtract(a, b): Subtract two numbers
        - multiply(a, b): Multiply two numbers
        - divide(a, b): Divide two numbers
        - power(base, exponent): Calculate base raised to exponent
        - sqrt(x): Calculate square root
        - abs(x): Calculate absolute value
        - factorial(n): Calculate factorial
        - mod(a, b): Calculate remainder
        - sin(x): Calculate sine (x in radians)
        - cos(x): Calculate cosine (x in radians)
        - tan(x): Calculate tangent (x in radians)
        """,
        name="system",
    ),
]


# Define tools
@tool
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    return a / b if b != 0 else float("inf")

@tool
def power(base: float, exponent: float) -> float:
    """Calculate base raised to exponent"""
    return base ** exponent

@tool
def sqrt(x: float) -> float:
    """Calculate square root"""
    if x < 0:
        return float('nan')
    return math.sqrt(x)

@tool
def abs(x: float) -> float:
    """Calculate absolute value"""
    return abs(x)

@tool
def factorial(n: int) -> int:
    """Calculate factorial"""
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial requires non-negative integer")
    return math.factorial(n)

@tool
def mod(a: float, b: float) -> float:
    """Calculate remainder"""
    if b == 0:
        return float('nan')
    return a % b

@tool
def sin(x: float) -> float:
    """Calculate sine (x in radians)"""
    return math.sin(x)

@tool
def cos(x: float) -> float:
    """Calculate cosine (x in radians)"""
    return math.cos(x)

@tool
def tan(x: float) -> float:
    """Calculate tangent (x in radians)"""
    return math.tan(x)

# Create list of all tools
all_tools = [add, subtract, multiply, divide, power, sqrt, abs, factorial, mod, sin, cos, tan]

# Add tools to a dictionary for reference
tools = {
    tool.name: tool for tool in all_tools
}

# Append math questions
messages.extend([
    HumanMessage(content="What is 2+2?", name="Sayem"),
    HumanMessage(content="What is 2-2?", name="Sayem"),
    HumanMessage(content="What is 2*2?", name="Sayem"),
    HumanMessage(content="What is 2/2?", name="Sayem"),
    HumanMessage(content="What is 2^3?", name="Sayem"),
    HumanMessage(content="What is √16?", name="Sayem"),
    HumanMessage(content="What is |−5|?", name="Sayem"),
    HumanMessage(content="What is 5!?", name="Sayem"),
    HumanMessage(content="What is 17 mod 5?", name="Sayem"),
    HumanMessage(content="What is sin(π/2)?", name="Sayem"),
    HumanMessage(content="What is cos(0)?", name="Sayem"),
    HumanMessage(content="What is tan(π/4)?", name="Sayem")
])

# Bind tools to the agent
agent = agent.bind_tools(all_tools)

# Invoke the agent with the messages
response = agent.invoke(messages)

# Extract and print tool calls
tool_calls = response.tool_calls
print("Tool Calls:")
print("-" * 100)
print(tool_calls)

print("\nAgent Response:")
print("-" * 100)
print(response.content)

print("\nTool Results:")
print("-" * 100)
# Process and invoke each tool call
if tool_calls:
    for call in tool_calls:
        try:
            tool_name = call["name"]
            tool_args = call["args"]
            if tool_name in tools:
                result = tools[tool_name].invoke(tool_args)
                print(f"Tool: {tool_name}, Args: {tool_args}, Result: {result}")
            else:
                print(f"Warning: Tool '{tool_name}' not found in available tools")
        except Exception as e:
            print(f"Error processing tool call {call}: {str(e)}")
