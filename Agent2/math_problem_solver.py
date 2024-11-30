from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.tools import tool

# Initialize the agent
agent = ChatOllama(model="hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF", temperature=0.7)

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
    print(f"Adding {a} and {b}")
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    print(f"Subtracting {a} and {b}")
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    print(f"Multiplying {a} and {b}")
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    print(f"Dividing {a} and {b}")
    return a / b if b != 0 else float("inf")  # Handle division by zero gracefully


# Add tools to a dictionary for reference
tools = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}

# Append math and general questions
messages.append(HumanMessage(content="what is 2+2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2-2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2*2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2/2?", name="Sayem"))
messages.append(HumanMessage(content="what is the capital of France?", name="Sayem"))

# Bind tools to the agent
agent = agent.bind_tools([add, subtract, multiply, divide])

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
