from PyQt5.QtCore import QObject, QJsonValue
from PyQt5.Qt import pyqtSlot, pyqtSignal

from multiprocessing import Process, Queue

import json


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


class UrlsObject(QObject):
    application = None

    def __init__(self, application):
        super().__init__()
        self.application = application

    @pyqtSlot(QJsonValue, result=list)
    def get_list(self, params):
        """

        :param QJsonValue params:
        :return:
        """
        params = params.toObject()
        if 'address' in params:
            params['address'] = params['address'].toString()
        if 'date_add' in params:
            params['date_add'] = params['date_add'].toObject()
            if 'from' in params['date_add']:
                params['date_add']['from'] = params['date_add']['from'].toString()
            if 'to' in params['date_add']:
                params['date_add']['to'] = params['date_add']['to'].toString()
        if 'last_visit' in params:
            params['last_visit'] = params['last_visit'].toObject()
            if 'from' in params['last_visit']:
                params['last_visit']['from'] = params['last_visit']['from'].toString()
            if 'to' in params['date_add']:
                params['last_visit']['to'] = params['last_visit']['to'].toString()
        if 'request_type' in params:
            if params['request_type'].isArray():
                params['request_type'] = [x.toString() for x in params['request_type'].toArray()]
            elif params['request_type'].isString():
                params['request_type'] = params['request_type'].toString()
        if 'is_active' in params:
            params['is_active'] = params['is_active'].toInt()
        if 'limit' in params:
            params['limit'] = params['limit'].toObject()
            if 'offset' in params['limit']:
                params['limit']['offset'] = params['limit']['offset'].toInt()
            if 'count' in params['limit']:
                params['limit']['count'] = params['limit']['count'].toInt()
        founded_urls = self.application.storage.urls.get(**params)
        result = []
        for x in founded_urls:
            result.append(x.to_dict())
        return result

    @pyqtSlot(int, result=list)
    def get_by_id(self, url_id):
        result = self.application.storage.urls.get_by_id(url_id)
        return [] if result is None else [result.to_dict()]
