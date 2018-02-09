import webbrowser

from application.storage import Storage
from browsers import ChromeBrowser
from errors import BrowserNotFound, BrowserNotSupport
from time import time
from re import match


class Application:
    available_browsers = []
    current_browsers = []
    loaded_browsers = {}
    storage = None

    def __init__(self):
        self.available_browsers = webbrowser._browsers
        self.storage = Storage()

    def get_browser(self, name):
        """
        :param name:
        :return:  Browser object
        :rtype: ChromeBrowser
        """
        if name not in self.available_browsers:
            raise BrowserNotFound(name)
        if name == 'chrome' or name == 'google-chrome':
            if 'chrome' not in self.loaded_browsers:
                self.loaded_browsers['chrome'] = ChromeBrowser(webbrowser.get(name))
            return self.loaded_browsers['chrome']
        else:
            raise BrowserNotSupport(name)

    def load_browser_history(self, browser):
        browser = self.get_browser(browser)
        history_generator = browser.get_history()
        for element in history_generator:
            url = self.storage.urls.create()
            url.address = element.url
            url.headers = element.headers
            url.cookies = []
            url.date_add = time()
            url.last_visit = 0
            url.request_type = 'GET'
            url.is_active = 1
            url.add_by = 'History import'
            if self.is_valid_url(url):
                url.save()
            else:
                del url
        self.storage.connection.commit()

    def is_valid_url(self, url):
        available_schemas = self.storage.options.get('available_schemas', [])
        blocked_domains = self.storage.options.get('blocked_domains', [])
        if url._parsed.scheme in available_schemas:
            for blocked_domain in blocked_domains:
                if match(blocked_domain, url._parsed.netloc) is not None:
                    return False
            return True
        return False
