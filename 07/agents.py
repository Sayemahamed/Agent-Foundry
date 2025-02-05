from langchain_groq import ChatGroq
from state import State
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

llm = ChatGroq(model="llama-3.3-70b-versatile",temperature=0.7)
def CEO_agent(state: State)->State:
    print("---CEO_agent---")
    response=llm.with_structured_output(schema={"message":str,"next":str}
                               ).invoke(
                                   [SystemMessage(content="HI")]
                                   +state["messages"]
                                   )
    return {"messages":[AIMessage( content=response["message"])],"next":response["next"]}

CEO_agent({"messages":[HumanMessage(content="HI")],"next":"CEO_agent"})