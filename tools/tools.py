from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str) -> str:
    """
    Searches for LinkedIn or Twitter profile page.

    Note, this function will not parse to only return the URL.
    But the llm is capable om extracting that information for us,
    so we do not have to do it here.
    """
    search = TavilySearchResults()
    results = search.run(name)

    return results
