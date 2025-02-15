from langchain_community.tools import TavilySearchResults
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from rich import print
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Session, Field, select

engine: Engine = create_engine(
    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)

with Session(bind=engine) as session:
    result = session.connection().exec_driver_sql(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    )
    for row in result:
        print(row[0])


class Data(SQLModel, table=True):
    url: str = Field(default=None, primary_key=True)
    content: str = Field(default=None)


SQLModel.metadata.create_all(engine)

with Session(bind=engine) as session:
    for data in session.exec(select(Data)).fetchmany(10):
        print(data)

with Session(bind=engine) as session:
    session.add(Data(url="https://example.com", content="Some details"))
    session.commit()


def get_listed_job_description(job_title):
    search = TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=False,
    )
    return search.invoke({"query": job_title})


temp = get_listed_job_description("machine learning tutorial filetype:pdf")
print(temp)
