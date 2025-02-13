from state06 import State, AgentResponse
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    AIMessage,
    HumanMessage,
    RemoveMessage,
)
from langgraph.types import Command
from typing import Literal
from rich import print
import sqlite3


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

cursor = sqlite3.connect("database.sqlite").cursor()


def get_database_info():
    database = []
    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    for row in tables:
        table_name = row[0]
        temp = []
        for column in cursor.execute(f"PRAGMA table_info({table_name})"):
            temp.append(column)
        database.append({f"{table_name}": temp})
    return database


print(get_database_info())
analyzer_prompt = f"""
## Role: Data Analyst in a Research Team  

You are a Data Analyst working within a Research Team that consists of a **Researcher, a Critic, and a Database Tool**.  

### Your Responsibilities:  
- You have access to the **database**, which contains tables and schema information in the format:  
  `{get_database_info()}` → `[table_name: [table_headers(info[])]]`  
- Your task is to **analyze the data and generate reports** based on user requests.  
- You can utilize the **Database Tool** to execute SQL queries and retrieve necessary data.  
- Your reports will be **reviewed by the Critic**, who will provide feedback for improvement.  

### Available Tools:  
1. **Database Tool** → Fetches data by executing SQL queries.  
2. **Critic** → Reviews your report and provides constructive feedback.  

Your goal is to provide clear, concise, and insightful reports based on the available database information. Use the feedback from the Critic to refine your analysis before delivering the final report.
###Example:

# Execute a SQL query to list all table names in the database, then move to the Database agent.
- `SELECT name FROM sqlite_master WHERE type='table';` next=Database

# Execute a SQL query to get the schema information of a specific table, then move to the Database agent.
- `PRAGMA table_info('table_name');` next=Database

# Submit the report to the Critic for review.
- `Your report` next=Critic

# Finalize and conclude the process and deliver the report.
- `Your report` next=END

### When ever calling the Database Tool, Give only the SQL query.
"""
critic_prompt = f"""\
## Role: Critic in a Research Team  

You are a Critic working within a Research Team that consists of a **Researcher, a Critic, and a Database Tool**.  

### Your Responsibilities:  
- You have access to the **Database Tool**, which contains tables and schema information in the format:  
  `{get_database_info()}` → `[table_name: [table_headers(info[])]]`  
- Your task is to **critique the reports** generated by the Data Analyst.  
- You can utilize the **Database Tool** to execute SQL queries and retrieve necessary data.  
- Your feedback will be **reviewed by the Data Analyst**, who will refine their analysis based on your suggestions.  

### Available Tools:  
1. **Database Tool** → Fetches data by executing SQL queries.  
2. **Data Analyst** → Generates reports based on your feedback.  

Your goal is to provide **constructive feedback** to the Data Analyst. Use your expertise to identify areas for improvement and suggest alternative approaches. ###Example:

- `SELECT name FROM sqlite_master WHERE type='table';` next=Database
  # The Database tool will execute the query and return the results to the Data Analyst.
- `PRAGMA table_info('table_name');` next=Database
  # The Database tool will execute the query and return the schema information of the table to the Data Analyst.
- `Your feedback` next=Analyst
  # The Data Analyst will receive your feedback and refine their report based on your suggestions.

### When ever calling the Database Tool, Give only the SQL query.
"""


def Analyzer_agent(state: State) -> Command[Literal["Critic", "Database", "__end__"]]:
    print("---Analyzer_agent---")
    state["criticized"] = state.get("criticized", 0)
    state["pre"] = state.get("pre", "Analyst")
    if state["criticized"] < 2:
        response = llm.with_structured_output(schema=AgentResponse).invoke(
            [SystemMessage(content=analyzer_prompt)] + state["messages"]
        )
    else:
        response = llm.with_structured_output(schema=AgentResponse).invoke(
            [SystemMessage(content=critic_prompt)]
            + state["messages"]
            + [
                HumanMessage(
                    content="Finalize and conclude the process and deliver the report."
                )
            ]
        )
    print("Analyzer_agent response:", response)
    if state["pre"] == "Database":
        return Command(
            update={
                "messages": [
                    AIMessage(content=response.message),
                    RemoveMessage(state["messages"][-1].id),
                ],
                "pre": "Analyst",
            },
            goto=response.next,
        )
    elif state["pre"] == "Critic":
        return Command(
            update={
                "messages": [AIMessage(content=response.message)],
                "pre": "Analyst",
                "criticized": state["criticized"] + 1,
            },
            goto=response.next if response.next != "END" else "__end__",
        )
    return Command(
        update={"messages": [AIMessage(content=response.message)], "pre": "Analyst"},
        goto=response.next,
    )


def Critic_agent(state: State) -> Command[Literal["Analyst", "Database"]]:
    print("---Critic_agent---")
    response = llm.with_structured_output(schema=AgentResponse).invoke(
        [SystemMessage(content=critic_prompt)] + state["messages"]
    )
    print("Critic_agent response:", response)
    if state["pre"] == "Database":
        return Command(
            update={
                "messages": [
                    AIMessage(content=response.message),
                    RemoveMessage(state["messages"][-1].id),
                ],
                "pre": "Critic",
            },
            goto=response.next,
        )
    return Command(
        update={"messages": [AIMessage(content=response.message)], "pre": "Critic"},
        goto=response.next,
    )


def Database_agent(state: State) -> Command[Literal["Analyst", "Critic"]]:
    print("---Database_agent---")
    cursor: sqlite3.Cursor = sqlite3.connect("database.sqlite").cursor()
    response = []
    try:
        for message in cursor.execute(str(state["messages"][-1].content)).fetchall():
            response.append(str(message))
    except sqlite3.Error as e:
        response.append(f"Database error: {e}")
    return Command(
        update={"messages": [AIMessage(content=str(response))], "pre": "Database"},
        goto=state["pre"],
    )
