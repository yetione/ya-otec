from fake_useragent import UserAgent
import os
from urllib.parse import urlparse


class Browser:
    _user_agents = None
    _browser = None

    def __init__(self, browser=None):
        self._user_agents = UserAgent()
        self._browser = browser


class Url:
    parsed = None
    headers = {}
    url = ''

    def __init__(self, url, **headers):
        self.parsed = urlparse(url)
        self.url = url
        self.headers = headers
