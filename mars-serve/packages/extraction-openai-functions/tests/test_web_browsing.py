import contextlib
from unittest import TestCase

from mars.tools.web_browsing import create_internet_search_tool, create_read_webpage_tool


class MockDDGS:
    def __init__(self):
        self.results = None

    def text(self, query: str, max_results: int):
        if self.results:
            return self.results
        return [f"{i}. Mock result '{query}'" for i in range(max_results)]


@contextlib.contextmanager
def mock_ddgs():
    yield MockDDGS()


class MockResponse:
    def __init__(self, body: str):
        self.content = bytes(f'<!doctype html><html><head></head><body>{body}</body></html>', 'utf-8')


def mock_requests_get(url: str) -> MockResponse:
    return MockResponse(f"Welcome to '{url}'")


class Test(TestCase):
    def test_internet_search(self):
        # noinspection PyTypeChecker
        mock_internet_search = create_internet_search_tool(mock_ddgs)
        results = mock_internet_search("APPL stock price")
        self.assertEqual([f"{i}. Mock result 'APPL stock price'" for i in range(5)], results)

    def test_read_webpage(self):
        mock_read_webpage = create_read_webpage_tool(mock_requests_get)
        content = mock_read_webpage("https://google.com")
        self.assertEqual("Welcome to 'https://google.com'", content)
