from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI
from state05 import State
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
import uuid

llm = ChatOpenAI(name="gpt-4o-mini", temperature=0)

def call(state:State,config:RunnableConfig,*,store:BaseStore):
    if "configurable" in config and "user_id" in config["configurable"]:
        user_id = config["configurable"]["user_id"]
    else:
        user_id = None
    namespace =("memories",user_id) if user_id else ("memories","Sayem")
    memories = store.search(namespace, query=str(state["messages"][-1].content))
    info = "\n".join([d.value["data"] for d in memories])
    system_msg = f"You are a helpful assistant talking to the user. User info: {info}"

    # Store new memories if the user asks the model to remember
    last_message = state["messages"][-1]
    if "remember" in last_message.content.lower(): #type:ignore
        memory = "User name is Sayem"
        store.put(namespace, str(uuid.uuid4()), {"data": memory})

    response: BaseMessage = llm.invoke(
        [{"role": "system", "content": system_msg}] + state["messages"]
    )
    return {"messages": response}