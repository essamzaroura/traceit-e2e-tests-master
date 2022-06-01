import requests
from hamcrest import *


class ApiHandler:

    def __init__(self, base_api_url, token):

        self.proxies = {"http": "http://proxy-chain.intel.com:911", "https": "https://proxy-chain.intel.com:911"}
        self.base_api_url = base_api_url
        self.header = {'Authorization': token}

    def set_header(self, heder):
        self.header = heder

    def set_proxies(self, proxies):
        self.proxies = proxies

    def set_base_api_url(self, url):
        self.base_api_url = url


    def get_api_response(self, url):
        url = f"{self.base_api_url}{url}"
        response = requests.get(url, proxies=self.proxies, headers=self.header)
        assert_that(response.status_code, equal_to(200),
                    "API request URL=[%s], content=[content=[%s],requestHeaders=[%s], INTERVAL=[%s] Failed!" % (
                        url, str(response.content.decode()), str(response.headers),
                        str(int(response.elapsed.total_seconds() * 3000)) + "ms"))

        return response.json()

    def post_api(self, url, body):
        url = f"{self.base_api_url}{url}"
        response = requests.post(url, json=body, proxies= self.proxies, headers=self.header)
        return response



