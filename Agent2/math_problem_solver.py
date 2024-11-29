from os import name
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.tools import tool

agent = ChatOllama(model="hf.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF", temperature=0.7)

messages: list[BaseMessage] = [
    SystemMessage(
        content="""
        You are Qwen, a math problem solver. You will be given a math problem and your task is to solve it using the tools provided.
        """,
        name="system",
    ),
]


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
    return a / b


tools = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}
messages.append(HumanMessage(content="what is 2+2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2-2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2*2?", name="Sayem"))
messages.append(HumanMessage(content="what is 2/2?", name="Sayem"))
for message in messages:
    message.pretty_print()


agent = agent.bind_tools([add, subtract, multiply, divide])
response = agent.invoke(messages).to_json()
tool_calls = response["kwargs"]["tool_calls"]
print(tool_calls)
for call in tool_calls:
    if call["type"] == "tool_call":
        print(tools[call["name"]](call["args"]))
