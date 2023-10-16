import json

from serpapi import GoogleSearch

from actions.action import Action


class SearchWeb(Action):
    def __init__(self, serpapi_key, query):
        self.serpapi_key = serpapi_key
        self.query = query

    async def execute(self):
        params = {
            "q": self.query,
            "api_key": self.serpapi_key,
            "num": "5",
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]
        return json.dumps(organic_results, indent=2)

    def __str__(self):
        return "search_web for query: " + self.query
