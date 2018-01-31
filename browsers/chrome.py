import os
from browsers import Browser, BrowserCantFindHistory
from browsers import BrowserCantFindBasePath
from browsers.history.sqlite import SQLiteHistory


class ChromeBrowser(Browser):

    name = 'Google Chrome'
    request_headers = {}
    user_agent = None
    _base_path = ''
    _possible_paths = (
        os.path.expanduser('~/.config/google-chrome/'),
        os.path.expanduser('~/.config/chromium/'),
        'C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\' % os.environ.get('USERNAME'),
        'C:\\Documents and Settings\\%s\\Local Settings\\Application Data\\Google\\Chrome\\' % os.environ.get(
            'USERNAME')
    )
    _history_path = ''
    _history_db = None

    def __init__(self):
        super().__init__()
        self.user_agent = self._user_agents.chrome
        self._load_data()

    def _load_data(self):
        for path in self._possible_paths:
            if os.path.exists(path):
                self._base_path = path
                history_path = os.path.join(path, 'Default', 'History')
                if os.path.exists(history_path):
                    self._history_path = history_path
                    self._history_db = SQLiteHistory(self._history_path, delete_db_copy=False)
                else:
                    raise BrowserCantFindHistory('Chrome')
                break
        else:
            raise BrowserCantFindBasePath('Chrome')

    def get_history(self, period=None):
        pass


