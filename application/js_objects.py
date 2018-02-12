from PyQt5.QtCore import QObject
from PyQt5.Qt import pyqtSlot, pyqtSignal

from multiprocessing import Process, Queue


class SpiderObject(QObject):
    application = None
    spider_running = False

    def __init__(self, application):
        super().__init__()
        self.application = application
        self.queue = Queue()
        self.task_done = pyqtSignal([dict], name='task_done')
        self.state_changed = pyqtSignal([bool], name='state_changed')

    @pyqtSlot(result=bool)
    def get_state(self):
        return self.application.spider_running

    @pyqtSlot(result=bool)
    def start(self):
        self.application.run_spider()
        return self.get_state()

    @pyqtSlot(result=bool)
    def stop(self):
        self.application.stop_spider()
        return self.get_state()

    @pyqtSlot(result=list)
    def get_data(self):
        if self.application.queue.empty():
            return []
        item = self.application.queue.get_nowait()
        return [item]
