import webbrowser

from errors import BrowserNotFound


class Application:
    available_browsers = []
    current_browsers = []



    def __init__(self):
        self.available_browsers = webbrowser._browsers


    def get_browser(self, name):
        if name not in self.available_browsers:
            raise BrowserNotFound(name)





