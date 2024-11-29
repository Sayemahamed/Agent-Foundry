from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json


@tool
def add(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: The first number
        b: The second number

    Returns:
        The sum of the numbers
    """
    print("addition called")
    return float(a) + float(b)


@tool
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first number.

    Args:
        a: The first number
        b: The second number to subtract

    Returns:
        The difference of the numbers
    """
    print("subtraction called")
    return float(a) - float(b)


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.

    Args:
        a: The first number
        b: The second number

    Returns:
        The product of the numbers
    """
    print("multiplication called")
    return float(a) * float(b)


@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number.

    Args:
        a: The dividend
        b: The divisor

    Returns:
        The quotient of the numbers
    """
    print("division called")
    b = float(b)
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return float(a) / b


@tool
def get_name() -> str:
    """Get the name of the user."""
    return "Fahim"


class Agent:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model="llama-3.2-3b-preview")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful AI assistant that performs math operations using tools.
                When you need to perform a calculation, output a JSON object with these fields:
                - tool: the name of the tool to use (add, subtract, multiply, or divide)
                - a: the first number
                - b: the second number

                For example, to add 2 and 3, output:
                {"tool": "add", "a": 2, "b": 3}

                Only output valid JSON when using tools. Otherwise, respond in natural language.""",
                ),
                ("human", "{input}"),
            ]
        )

        self.tools = {
            "add": add,
            "subtract": subtract,
            "multiply": multiply,
            "divide": divide,
            "get_name": get_name,
        }

    def chat(self, message: str):
        # Format the message using the prompt template
        messages = self.prompt.format_messages(input=message)

        # Get response from LLM
        response = self.llm.invoke(messages)
        content = response.content

        try:
            # Try to parse as JSON
            data = json.loads(content)
            if "tool" in data and data["tool"] in self.tools:
                tool = self.tools[data["tool"]]
                result = tool(data["a"], data["b"])
                return f"The result is {result}"
            return content
        except json.JSONDecodeError:
            # If not JSON, return the response as is
            return content


agent = Agent()
print(agent.chat("what is 2 + 2 ?"))
