from PyQt5.Qt import QWebEnginePage, pyqtSlot, pyqtSignal
# from application.application import Application
import json


class WebPage(QWebEnginePage):
    application = None
    """
    :type: Application
    """

    def __init__(self, profile, parent):
        super(WebPage, self).__init__(profile, parent)
        self.selectionChanged.emit()

    def urlEvent(self):
        pass

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        try:
            print('%s:%s: %s' % (source_id, linenumber, msg))
        except OSError:
            pass

    @pyqtSlot(str)
    def print(self, text):
        print('From JS:', text)

    @pyqtSlot(int, int, result=list)
    def get_urls(self, offset, count):
        result = []
        for url in self.application.storage.urls.get(limit={'count': count, 'offset': offset}):
            result.append({'id': url.id, 'url': url.address, 'headers': url.headers, 'last_visit': url.last_visit})
        return result
