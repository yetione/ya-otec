from grab.spider import Spider, Task, Data
from grab import Grab
from time import sleep

from re import match

from application.storage import Storage
from browsers import Url


class ShumSpider(Spider):
    task_interval = 1
    history_args = {}
    url_result = None
    visited = []
    storage = None
    queue = None
    """
    :type: Queue
    """
    def get_urls(self, grab):
        links = grab.doc.tree.xpath('//a/@href')
        for i, link in enumerate(links):
            links[i] = Url(grab.make_url_absolute(link),  **{'User-Agent': self.browser.user_agent})
        return links

    def run(self, queue):
        self.queue = queue
        super(ShumSpider, self).run()

    def stop(self):
        super(ShumSpider, self).stop()

    def task_generator(self):
        self.visited = []
        self.storage = Storage()
        url_result = self.storage.urls.get()
        for element in url_result:
            url = element.get_url()
            if url in self.visited:
                continue
            g = Grab()
            g.setup(url=url, headers=element.headers)
            self.visited.append(url)
            yield Task('history_element', grab=g, visit_deep=False)

    def task_history_element(self, grab, task):
        print(task.url)
        self.queue.put_nowait({'url': task.url})
        sleep(self.task_interval)
        if task.visit_deep:
            links = self.get_urls(grab)

            for element in links:
                url = element.get_url()
                if self.is_valid_url(url) and url not in self.visited:
                    g = Grab()
                    g.setup(url=url, headers={'User-Agent': element.headers['User-Agent']})
                    self.application.visited.append(url)
                    yield Task('history_element', grab=g)

        # print(grab.doc.cookies.get_dict())

    def is_valid_url(self, url):
        available_schemas = self.storage.options.get('available_schemas', [])
        blocked_domains = self.storage.options.get('blocked_domains', [])
        if url._parsed.scheme in available_schemas:
            for blocked_domain in blocked_domains:
                if match(blocked_domain, url._parsed.netloc) is not None:
                    return False
            return True
        return False
