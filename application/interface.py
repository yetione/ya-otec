from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QWebEngineView, QWebEngineScript, QIODevice, QFile, QWebChannel

from application.webpage import WebPage


class Interface:
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(904, 599)
        self.web_enige = QWebEngineView(MainWindow)
        self.web_enige.resize(904, 599)
        MainWindow.setCentralWidget(self.web_enige)
        self.web_page = WebPage()


