import webbrowser

from grab import Grab
from grab.spider import Task

from application.storage import Storage
from browsers import ChromeBrowser
from browsers.firefox import FirefoxBrowser
from browsers.opera import OperaBrowser
from errors import BrowserNotFound, BrowserNotSupport
from time import time
from re import match

from spider import ShumSpider


class Application:
    available_browsers = []
    current_browsers = []
    loaded_browsers = {}
    storage = None
    visited = []

    """
    :type: ShumSpider
    """
    spider = None

    def __init__(self):
        self.available_browsers = webbrowser._browsers
        self.storage = Storage()
        self.spider = ShumSpider(thread_number=10)
        self.spider.task_interval = self.storage.options.get('task_interval', 1)

    def get_browser(self, name):
        """
        :param name:
        :return:  Browser object
        :rtype: ChromeBrowser
        """
        if name == 'chrome' or name == 'google-chrome':
            if 'chrome' not in self.loaded_browsers:
                self.loaded_browsers['chrome'] = ChromeBrowser(None)
            return self.loaded_browsers['chrome']
        elif name == 'firefox':
            if 'firefox' not in self.loaded_browsers:
                self.loaded_browsers['firefox'] = FirefoxBrowser(webbrowser.get(name))
            return self.loaded_browsers['firefox']
        elif name == 'opera':
            if 'opera' not in self.loaded_browsers:
                self.loaded_browsers['opera'] = OperaBrowser(webbrowser.get(name))
            return self.loaded_browsers['opera']
        else:
            raise BrowserNotSupport(name)

    def load_browser_history(self, browser):
        browser = self.get_browser(browser)
        history_generator = browser.get_history()
        loaded_elements = 0
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
                if url.save():
                    loaded_elements += 1
                else:
                    print('Cant save history element ' + element.url)
            else:
                del url
        self.storage.connection.commit()
        return loaded_elements

    def run_spider(self, count=None):
        self.spider.application = self
        self.spider.setup_queue()
        if count is None:
            url_result = self.storage.urls.get()
        else:
            url_result = self.storage.urls.get(limit={'count':count})
        for element in url_result:
            url = element.get_url()
            if url in self.visited:
                continue
            g = Grab()
            g.setup(url=url, headers=element.headers)
            self.spider.add_task(Task('history_element', grab=g, visit_deep=False))
            self.visited.append(url)
        self.spider.run()

    def is_valid_url(self, url):
        available_schemas = self.storage.options.get('available_schemas', [])
        blocked_domains = self.storage.options.get('blocked_domains', [])
        if url._parsed.scheme in available_schemas:
            for blocked_domain in blocked_domains:
                if match(blocked_domain, url._parsed.netloc) is not None:
                    return False
            return True
        return False
