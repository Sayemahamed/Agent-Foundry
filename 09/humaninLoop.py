from langgraph.func import entrypoint, task
from langgraph.types import Command, interrupt


@task
def step_1(input_query):
    """Append bar."""
    return f"{input_query} bar"


@task
def human_feedback(input_query):
    """Append user input."""
    feedback = interrupt(f"Please provide feedback: {input_query}")
    return f"{input_query} {feedback}"


@task
def step_3(input_query):
    """Append qux."""
    return f"{input_query} qux"


from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()


@entrypoint(checkpointer=checkpointer)
def graph(input_query):
    result_1 = step_1(input_query).result()
    result_2 = human_feedback(result_1).result()
    result_3 = step_3(result_2).result()

    return result_3


async for chunk in graph.astream(
    input="foo", config={"configurable": {"thread_id": "1"}}
):
    print(chunk)


async for chunk in graph.astream(
    Command(resume="yo"), config={"configurable": {"thread_id": "1"}}
):
    print(chunk)
