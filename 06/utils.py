from langchain_openai import ChatOpenAI
from state06 import AgentResponse
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
import json
from rich import print
import sqlite3
# print(AgentResponse.model_fields)
# print(json.dumps(AgentResponse.model_json_schema(), indent=0))

# AgentResponse.model_validate_strings('{"Message": "The report should include a comparison of trends.", "Next": "Data Analyst"}')

llm = ChatOpenAI(name="gpt-4o-mini", temperature=0)


def invoke_llm(prompt: list[AnyMessage], count: int = 0) -> AgentResponse:
    if count > 2:
        raise Exception("Too many attempts to parse response")
    response: AIMessage = llm.invoke(prompt)  # type: ignore
    print("""---""" * 80)
    print(prompt)
    print("""---""" * 80)
    print(response.content)
    print("""---""" * 80)
    try:
        response_json = json.loads(str(response.content))
        return AgentResponse.model_validate(response_json)
    except Exception as e:
        validation_schema: str = json.dumps(AgentResponse.model_json_schema(), indent=2)
        return invoke_llm(
            [
                AIMessage(content=response.content),
                HumanMessage(
                    content=f"Give the previous response as valid JSON response that matches this schema:\n{validation_schema} Give Only JSON , no other text, not even in Markdown"
                ),
            ],
            count=count + 1,
        )


cursor: sqlite3.Cursor = sqlite3.connect(database="database.sqlite").cursor()


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


if __name__ == "__main__":
    print(
        invoke_llm(
            [
                HumanMessage(
                    content="What is the best next step after analyzing user data?"
                )
            ]
        )
    )
