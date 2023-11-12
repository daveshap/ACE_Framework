import asyncio

import httpx
from dotenv import load_dotenv

from util import get_environment_variable


class GiphyFinder:
    def __init__(self, giphy_api_key):
        self.giphy_api_key = giphy_api_key

    async def get_giphy_url(self, query: str):
        url = f'https://api.giphy.com/v1/gifs/translate?api_key={self.giphy_api_key}&s={query}&limit=1'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            gif_url = data['data']['images']['original']['url']
            return gif_url
        else:
            print(f'Failed to retrieve GIF: {response.status_code}')
            return None


if __name__ == "__main__":
    load_dotenv()
    giphy_filter = GiphyFinder(get_environment_variable('GIPHY_API_KEY'))
    print(asyncio.run(giphy_filter.get_giphy_url('funny cat')))
