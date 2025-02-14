from langchain_community.tools import TavilySearchResults
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
import psycopg
from rich import print
from sqlalchemy import Engine
from sqlmodel import SQLModel,create_engine,Session,Field
engine: Engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/postgres")

with Session(engine) as session:
    result = session.connection().exec_driver_sql(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    )
    for row in result:
        print(row[0])

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
# Establish connection
try:
    print("Connected to TimescaleDB successfully!")

    # Create a cursor object
    cur = conn.cursor()

    # Example query: Check PostgreSQL version
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Database Version:", version)
    # Show all tables
    cur.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
    )
    tables = cur.fetchall()
    print("Tables in the database:")
    for table in tables:
        print("-", table[0])
    # Close cursor and connection
    cur.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Error:", e)
