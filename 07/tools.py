from langchain_community.tools import TavilySearchResults

# Configure the search tool with desired parameters
tavily = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=False,
    include_raw_content=False,
    include_images=False,
    # Optionally include or exclude specific domains:
    # include_domains=[...],
    # exclude_domains=[...],
    # Optionally override default name/description:
    # name="CustomSearchTool",
    # description="A tool for advanced internet search results.",
    # Optionally override the default args_schema:
    # args_schema=...
)
def tool(topic:str):
    """
    Searches the internet for the given topic and returns the results.
    
    Parameters
    ----------
    topic : str
        The topic to search for.
    
    Returns
    -------
    str
        The search results.
    """
    temp =tavily.run(topic)
    print(temp)
    return temp