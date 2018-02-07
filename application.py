import webbrowser
from time import time, sleep

from grab import Grab
from grab.spider import Task

from browsers import ChromeBrowser
from errors import BrowserNotFound, BrowserNotSupport
from spider import ShumSpider


class Application:
    available_browsers = []
    current_browsers = []
    loaded_browsers = {}
    spider = None
    restricted_parts = ['127.0.0', '//localhost', '//google.ru/', '//google.com/', '.local/', '//192.168',
                        '//www.google.ru',
                        '//www.google.com', '//yandex.ru', '//www.yandex.ru', '//vk.com', '//www.vk.com']
    visited = {}

    def __init__(self):
        self.available_browsers = webbrowser._browsers
        self.spider = ShumSpider(thread_number=10)

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

    def run_spider(self):
        browser = self.get_browser('google-chrome')
        history_generator = browser.get_history(limit={'count': 1}, order_by=['RANDOM()'])
        self.spider.browser = browser
        self.spider.application = self
        self.spider.setup_queue()
        for element in history_generator:
            url = element.get_url()
            if not self.is_valid_url(url) or url in self.visited:
                continue
            g = Grab()
            g.setup(url=url, headers={'User-Agent': element.headers['User-Agent']})
            self.spider.add_task(Task('history_element', grab=g))
            self.visited[url] = 1
        #self.spider.set_history(history_generator)
        self.spider.run()

    def is_valid_url(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            for part in self.restricted_parts:
                try:
                    url.index(part)
                    return False
                except ValueError:
                    continue
            return True
        return False

    def stop_spider(self):
        self.spider.stop()
