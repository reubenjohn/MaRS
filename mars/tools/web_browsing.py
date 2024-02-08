from typing import Type, Callable

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain.tools import tool


def create_internet_search_tool(search_api: Type[DDGS]) -> Callable:
    @tool("internet_search", return_direct=False)
    def internet_search_tool(query: str) -> str:
        """Searches the internet using DuckDuckGo."""
        print(f"internet_search({query})")
        with search_api() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            print(f"internet_search results: {results}")
            return results if results else "No results found."

    return internet_search_tool


internet_search = create_internet_search_tool(DDGS)


def create_read_webpage_tool(fetch_url_fn: Callable) -> Callable:
    @tool("read_webpage", return_direct=False)
    def read_webpage_tool(url: str) -> str:
        """Processes content from a webpage."""
        print(f"read_webpage({url})")
        response = fetch_url_fn(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        print(f"read_webpage results: <omitted {len(text)} characters of content>")
        return text

    return read_webpage_tool


read_webpage = create_read_webpage_tool(requests.get)
