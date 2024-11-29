from langchain_ollama import ChatOllama
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.memory import ConversationBufferMemory


class Agent:
    def __init__(self):
        self.llm = ChatOllama(
            temperature=0, model="hf.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF",format="json"
        )
        self.memory = ConversationBufferMemory(return_messages=True)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are a helpful AI assistant."
                ),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

    def chat(self, message: str):
        # Get conversation history
        history = self.memory.load_memory_variables({})["history"]

        # Format the message using the prompt template
        messages = self.prompt.format_messages(input=message, history=history)
        print(messages)

        # Get response from LLM
        response = self.llm.invoke(messages)

        # Save the conversation
        self.memory.save_context({"input": message}, {"output": response.content})

        return response.content


agent = Agent()
print(agent.chat("what is my name ?"))
