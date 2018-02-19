import webbrowser

from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import QWebEngineView, QWebEngineScript, QIODevice, QFile, QWebChannel, QWebEngineProfile, QWebEngineSettings
from grab import Grab
from grab.spider import Task
from os.path import realpath, getmtime, exists
from multiprocessing import Process
from time import time, sleep
from re import match
from jinja2 import Environment, FileSystemLoader

from application.storage import Storage
from application.webpage import WebPage
from browsers import ChromeBrowser
from browsers.firefox import FirefoxBrowser
from browsers.opera import OperaBrowser
from errors import BrowserNotFound, BrowserNotSupport
import logging

from spider import ShumSpider
from application.js_objects import *
# from application.thread import SpiderThread


class Application(QMainWindow):
    available_browsers = []
    current_browsers = []
    loaded_browsers = {}
    force_compile = True
    storage = None
    visited = []
    spider_running = False
    spider = None
    """
        :type: ShumSpider
    """

    def __init__(self, parent=None):
        super(Application, self).__init__(parent)

        self.available_browsers = webbrowser._browsers
        self.storage = Storage()
        self.spider = self.create_spider()
        self.spider.task_interval = self.storage.options.get('task_interval', 1)
        self.spider_process = Process(target=self.spider.run)
        self.spider_object = SpiderObject(self)
        self.urls_object = UrlsObject(self)
        self.force_compile = True
        self.queue = Queue()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName('MainWindow')
        self.resize(1000, 600)
        
        self.web_view = QWebEngineView(self)
        self.web_view.resize(1000, 600)
        self.setCentralWidget(self.web_view)
        
        self.web_profile = QWebEngineProfile(self.web_view)
        self.web_profile.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        
        self.web_page = WebPage(self.web_profile, self)
        self.web_page.application = self
        self.web_view.setPage(self.web_page)

        self.chanel = QWebChannel(self.web_page)
        self.web_page.setWebChannel(self.chanel)
        self.chanel.registerObject('bridge', self.web_page)
        self.chanel.registerObject('spider', self.spider_object)
        self.chanel.registerObject('urls', self.urls_object)
        self.set_page()

    def set_page(self):
        if self.force_compile or not exists(realpath('./data/compiled/index.html')) or \
                getmtime(realpath('./interface/index.html')) > getmtime(realpath('./data/compiled/index.html')):
            self._compile_template('index.html', './data/compiled/index.html')
        qFile_page = QFile(realpath('./data/compiled/index.html'))
        self.web_view.load(QUrl.fromLocalFile(QFileInfo(qFile_page).absoluteFilePath()))
        self.web_page.selectionChanged.emit()

    @staticmethod
    def _compile_template(template, output):
        env = Environment(loader=FileSystemLoader('./interface'))
        template = env.get_template(template)
        file = open(realpath(output), 'w')
        file.write(template.render(basepath='../../interface'))
        file.close()

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
        if not self.spider_running:
            self.queue = Queue()
            self.spider_process = Process(target=self._start_spider, args=(count, self.queue))
            self.spider_running = True
            self.spider_process.start()
            logger = logging.getLogger('shum.app')
            logger.debug('Spider running')

    def _start_spider(self, count, queue):
        self.spider = self.create_spider()
        self.spider.application = self
        self.spider.history_args = {'limit': {'count': count}}
        self.spider.run(queue)

    def stop_spider(self):
        if self.spider_running:
            self.spider_running = False
            self.spider_process.terminate()
            self.spider.stop()
            logger = logging.getLogger('shum.app')
            logger.debug('Spider stopped')

    @staticmethod
    def create_spider():
        return ShumSpider(thread_number=10, transport='threaded')

    def is_valid_url(self, url):
        available_schemas = self.storage.options.get('available_schemas', [])
        blocked_domains = self.storage.options.get('blocked_domains', [])
        if url._parsed.scheme in available_schemas:
            for blocked_domain in blocked_domains:
                if match(blocked_domain, url._parsed.netloc) is not None:
                    return False
            return True
        return False
