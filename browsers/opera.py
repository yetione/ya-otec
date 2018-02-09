import os

from browsers import ChromeBrowser


class OperaBrowser(ChromeBrowser):
    name = 'Opera'
    request_headers = {}
    user_agent = None
    _base_path = ''
    _possible_paths = (
        os.path.expanduser('~/.config/opera/'),
        'C:\\Users\\%s\\AppData\\Local\\Opera\\Opera\\' % os.environ.get('USERNAME'),
        'C:\\Users\\%s\\AppData\\Roaming\\Opera\\Opera\\' % os.environ.get('USERNAME'),
        'C:\\Documents and Settings\\%s\\Local Settings\\Application Data\\Opera\\Opera\\' % os.environ.get(
            'USERNAME')
    )
    _history_path = ''
    _history_db = None

    def __init__(self, browser):
        super().__init__(browser)
        self.user_agent = self._user_agents.opera
        self._load_data()

    @staticmethod
    def _get_history_file(path):
        return os.path.join(path, 'History')
