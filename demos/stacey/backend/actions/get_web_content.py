import httpx
from bs4 import BeautifulSoup

from actions.action import Action


class GetWebContent(Action):
    def __init__(self, url):
        self.url = url

    async def execute(self):
        print("GetWebContent: Executing GetWebContent with url: " + self.url)
        web_content = await get_compressed_web_content(self.url)
        print("GetWebContent: Returning web content: " + web_content[:100] + "...")
        return web_content

    def __str__(self):
        return "get_web_content for url: " + self.url


async def get_compressed_web_content(url) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements_to_remove = ['script', 'style', 'head', 'svg']
        for script_or_style in soup(elements_to_remove):
            script_or_style.extract()
        for tag in soup.find_all(True):
            tag.attrs = {}
        return soup.prettify()

if __name__ == '__main__':
    import asyncio

    async def main():
        url = 'https://raw.githubusercontent.com/daveshap/ACE_Framework/main/demos/stacey/docs/test_scenarios.md'
        content = await GetWebContent(url).execute()
        print(content)

    asyncio.run(main())
