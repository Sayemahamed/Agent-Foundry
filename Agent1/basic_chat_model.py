from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama


class Agent:
    def __init__(self):
        self.llm = ChatOllama(
            model="hf.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF", temperature=0.7
        )

    def respond(self, message):
        return self.llm.invoke(
            [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=message),
            ]
        )


agent = Agent()
agent.respond("What is the capital of France?").to_json()
