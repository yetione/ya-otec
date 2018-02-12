from multiprocessing import Process

from spider import ShumSpider


class SpiderProcess(Process):
    spider = None

    def run(self):
        spider = ShumSpider(thread_number=10, transport='threaded')
        super(SpiderProcess, self).run()

    def terminate(self):
        super(SpiderProcess, self).terminate()