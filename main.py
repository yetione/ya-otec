from PyQt5.QtWidgets import QApplication

from application.application import Application
from application.log import logger

import sys
if sys.platform.startswith('linux'):
    from OpenGL import GL

if __name__ == '__main__':
    _app = QApplication([])

    app = Application()
    app.show()
    _app.exec_()

    #try:
    #    app.run_spider()
    #except KeyboardInterrupt:
    #    pass
    #print(app.spider.render_stats())
    #app.stop_spider()