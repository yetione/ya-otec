from grab.spider import Spider, Task, Data
from grab import Grab
import browsers
import webbrowser

from application import Application


class ShumSpider(Spider):

    def task_generator(self):
        print('ss')
        g = Grab()

        yield Task('test', url='https://spb.showgogo.ru/events/festivals/mayatnik-fuko/')

    def task_test(self, grab, task):
        print('s2')


if __name__ == '__main__':
    app = Application()
    try:
        app.run_spider()
    except KeyboardInterrupt:
        pass
    print(app.spider.render_stats())
    app.stop_spider()