from grab.spider import Spider, Task, Data
from grab import Grab
import browsers


class ShumSpider(Spider):

    def task_generator(self):
        print('ss')
        g = Grab()

        yield Task('test', url='https://spb.showgogo.ru/events/festivals/mayatnik-fuko/')

    def task_test(self, grab, task):
        print('s2')


if __name__ == '__main__':
    bot = ShumSpider(thread_number=10)

    try:
        bot.run()
    except KeyboardInterrupt:
        pass
    print(bot.render_stats())