from fake_useragent import UserAgent
import os
from urllib.parse import urlparse

class Browser:
    _user_agents = None


    def __init__(self):
        self._user_agents = UserAgent()

class Url:
    parsed = None
    headers = {}

    def __init__(self, url, **headers):
        self.parsed = urlparse(url)
        self.headers = headers





