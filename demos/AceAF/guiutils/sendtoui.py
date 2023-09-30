# api_client.py

import requests


class ApiClient:
    BASE_URL = 'http://127.0.0.1:5000/'

    def __init__(self):
        pass
        # self.endpoints = {
        #     'api1': 'api1',
        #     'api2': 'api2',
        #     'api3': 'api3'
        # }

    def send_message(self, target, message):
        # if target not in self.endpoints:
        #     raise ValueError(f"Invalid target: {target}. Valid targets are: {', '.join(self.endpoints.keys())}")

        # url = self.BASE_URL + self.endpoints[target]
        url = self.BASE_URL + target
        print(f"\nSending message to {url}: {message}")
        response = requests.post(url, json={'message': message})
        print(f"\nResponse: {response}")

        return response.json()


# Example usage:
if __name__ == "__main__":
    client = ApiClient()

    # Send a message to api1
    response = client.send_message('api1', 'Hello to API 1!')
    print(response)

    # Send a message to api2
    response = client.send_message('api2', 'Hello to API 2!')
    print(response)

    # Send a message to api3
    response = client.send_message('api3', 'Hello to API 3!')
    print(response)
