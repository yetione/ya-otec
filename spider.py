from grab.spider import Spider, Task, Data
from grab import Grab


class ShumSpider(Spider):
    browser = None
    history = None

    def set_history(self, history):
        self.history = history

    def task_history_element(self, grab, task):
        print(grab.response)
