from langchain_community.tools import TavilySearchResults
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from rich import print
from sqlalchemy import Engine
import os
from sqlmodel import SQLModel, create_engine, Session, Field, select
from dotenv import load_dotenv
load_dotenv()

engine: Engine = create_engine(
    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)


SQLModel.metadata.create_all(engine)

class Job(SQLModel, table=True):
    url: str = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: str = Field(default=None)




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
