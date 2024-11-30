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
    return a / b if b != 0 else float("inf")  # Handle division by zero gracefully


@tool
def power(base: float, exponent: float) -> float:
    """Calculate base raised to the power of exponent"""
    return base ** exponent


@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    if x < 0:
        return float('nan')  # Return NaN for negative numbers
    return math.sqrt(x)


@tool
def absolute_value(x: float) -> float:
    """Calculate the absolute value of a number"""
    return abs(x)


@tool
def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer"""
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial is only defined for non-negative integers")
    if n == 0:
        return 1
    return math.factorial(n)


@tool
def modulo(a: float, b: float) -> float:
    """Calculate the remainder when a is divided by b"""
    if b == 0:
        return float('nan')  # Return NaN for division by zero
    return a % b


@tool
def sin(x: float) -> float:
    """Calculate the sine of an angle in radians"""
    return math.sin(x)


@tool
def cos(x: float) -> float:
    """Calculate the cosine of an angle in radians"""
    return math.cos(x)


@tool
def tan(x: float) -> float:
    """Calculate the tangent of an angle in radians"""
    return math.tan(x)


# Add tools to a dictionary for reference
tools = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "power": power,
    "square_root": square_root,
    "absolute_value": absolute_value,
    "factorial": factorial,
    "modulo": modulo,
    "sin": sin,
    "cos": cos,
    "tan": tan
}


# Append math and general questions
messages.append(HumanMessage(content="what is 2+2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2-2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2*2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2/2?", name="Sayem"))
messages.append(HumanMessage(content="what is the capital of France?", name="Sayem"))
messages.append(HumanMessage(content="What is 2 to the power of 3?", name="Sayem"))
messages.append(HumanMessage(content="What is the square root of 16?", name="Sayem"))
messages.append(HumanMessage(content="What is the absolute value of -5?", name="Sayem"))
messages.append(HumanMessage(content="Calculate factorial of 5", name="Sayem"))
messages.append(HumanMessage(content="What is 17 modulo 5?", name="Sayem"))
messages.append(HumanMessage(content="What is the sine of 90 degrees in radians?", name="Sayem"))
messages.append(HumanMessage(content="What is the cosine of 0 radians?", name="Sayem"))
messages.append(HumanMessage(content="Solve this complex expression: (2^3 + 4) * |−2|", name="Sayem"))
messages.append(HumanMessage(content="Calculate the hypotenuse of a right triangle with sides 3 and 4", name="Sayem"))

# Bind tools to the agent
agent = agent.bind_tools([add, subtract, multiply, divide, power, square_root, 
                         absolute_value, factorial, modulo, sin, cos, tan])

# Invoke the agent with the messages
response = agent.invoke(messages)

# Extract and print tool calls
tool_calls = response.tool_calls
print(tool_calls)

print("-" * 100)

# Print agent's final response
content = response.content
print(content)

print("-" * 100)

# Process and invoke each tool call
for call in tool_calls:
    tool_name = call["name"]
    tool_args = call["args"]
    result = tools[tool_name].invoke(tool_args)  # Correctly unpack arguments
    print(f"Tool: {tool_name}, Result: {result}")
