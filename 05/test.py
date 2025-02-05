import sqlite3

con: sqlite3.Cursor = sqlite3.connect(database="database.sqlite").cursor()
def database(str: str) -> list[tuple]:
    """
    Executes a SQL query on the connected SQLite database and retrieves all results.

    Parameters:
        str (str): The SQL query to execute.

    Returns:
        list[tuple]: A list of tuples containing the results of the query.
    """
    print(str)
    return con.execute(str).fetchall()


database("SELECT name FROM sqlite_master WHERE type='table';")

for table in database("SELECT name FROM sqlite_master WHERE type='table';"):
    print(table[0])
    print(database(f"PRAGMA table_info({table[0]})"))

