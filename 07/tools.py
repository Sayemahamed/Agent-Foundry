from langchain_community.tools import TavilySearchResults, DuckDuckGoSearchResults
import wikipedia

# Configure Tavily Search Tool
tavily = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=False,
    include_raw_content=False,
    include_images=False,
    # Optionally include or exclude specific domains,
    # Optionally override default name/description or args_schema
)

def tavily_tool(topic: str) -> str:
    """
    Searches the internet using TavilySearchResults for the given topic.
    
    Parameters
    ----------
    topic : str
        The topic to search for.
    
    Returns
    -------
    str
        The search results as a string.
    """
    result = tavily.invoke({"query": topic})
    print("Tavily Search Results:", result)
    return result

# Configure DuckDuckGo Search Tool
duck = DuckDuckGoSearchResults(
    max_results=5
    # Additional parameters can be set here if required
)

def duck_tool(topic: str) -> str:
    """
    Searches the internet using DuckDuckGo for the given topic.
    
    Parameters
    ----------
    topic : str
        The topic to search for.
    
    Returns
    -------
    str
        The search results as a string.
    """
    result = duck.invoke({"query": topic})
    print("DuckDuckGo Search Results:", result)
    return result

def wikipedia_tool(topic: str) -> str:
    """
    Retrieves a summary for the given topic from Wikipedia.
    
    Parameters
    ----------
    topic : str
        The topic to search on Wikipedia.
    
    Returns
    -------
    str
        A summary of the topic from Wikipedia.
    """
    try:
        summary = wikipedia.summary(topic, sentences=3)
        print("Wikipedia Summary:", summary)
        return summary
    except Exception as e:
        error_message = f"Error retrieving Wikipedia summary: {e}"
        print(error_message)
        return error_message

# Example usage:
if __name__ == "__main__":
    search_topic = "vector databases"
    
    print("=== Tavily Search ===")
    tavily_result = tavily_tool(search_topic)
    
    print("\n=== Wikipedia Summary ===")
    wiki_result = wikipedia_tool(search_topic)
    
    print("\n=== DuckDuckGo Search ===")
    duck_result = duck_tool(search_topic)
