from typing import Dict, Any

import requests
from bs4 import BeautifulSoup

from tools.tool import Tool


class WebTool(Tool):
    def use_tool(self, params: Dict[str, Any]) -> str:
        """
        Fetches and compresses web content for a given URL.

        Args:
        - params (Dict[str, Any]): Must contain 'url' key with the URL to fetch.

        Returns:
        - str: Compressed web content.
        """
        url = params.get('url')
        if not url:
            raise ValueError("url not provided in parameters.")

        return get_compressed_web_content(url)


def get_compressed_web_content(url) -> str:
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements_to_remove = ['script', 'style', 'head', 'svg']
    for script_or_style in soup(elements_to_remove):
        script_or_style.extract()
    for tag in soup.find_all(True):
        tag.attrs = {}
    return soup.prettify()


if __name__ == '__main__':
    print(get_compressed_web_content('https://raw.githubusercontent.com/daveshap/ACE_Framework/main/demos/stacey/docs/test_scenarios.md'))