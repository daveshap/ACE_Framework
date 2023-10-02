from bs4 import BeautifulSoup
import requests


def get_compressed_web_content(url):
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