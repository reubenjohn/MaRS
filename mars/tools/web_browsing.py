import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain.tools import tool


@tool("internet_search", return_direct=False)
def internet_search(query: str) -> str:
    """Searches the internet using DuckDuckGo."""
    print(f"internet_search({query})")
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
        print(f"internet_search results: {results}")
        return results if results else "No results found."


@tool("read_webpage", return_direct=False)
def read_webpage(url: str) -> str:
    """Processes content from a webpage."""
    print(f"process_content({url})")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    print(f"process_content results: {text}")
    return text
