import webbrowser
from time import time

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
        history_generator = browser.get_history(limit={'count': 20})
        self.spider.setup_queue()
        for element in history_generator:
            g = Grab()
            g.setup(headers={'User-Agent': element.headers['User-Agent']})
            print(element.url)
            self.spider.add_task(Task('history_element', url=element.url, grab=g))
        #self.spider.set_history(history_generator)
        self.spider.run()

    def stop_spider(self):
        self.spider.stop()
