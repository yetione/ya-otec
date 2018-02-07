from grab.spider import Spider, Task, Data
from grab import Grab
from time import sleep
from browsers import Url


class ShumSpider(Spider):
    browser = None
    history = None
    application = None

    def set_history(self, history):
        self.history = history

    def get_urls(self, grab):
        links = grab.doc.tree.xpath('//a/@href')
        for i, link in enumerate(links):
            links[i] = Url(grab.make_url_absolute(link),  **{'User-Agent': self.browser.user_agent})
        return links

    def task_history_element(self, grab, task):
        print(task.url)
        links = self.get_urls(grab)
        # sleep(.5)
        for element in links:

            url = element.get_url()
            if self.application.is_valid_url(url) and url not in self.application.visited:
                g = Grab()
                g.setup(url=url, headers={'User-Agent': element.headers['User-Agent']})
                self.application.visited[url] = 1
                yield Task('history_element', grab=g)

        # print(grab.doc.cookies.get_dict())
