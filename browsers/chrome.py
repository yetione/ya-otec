import os
from browsers import Browser, \
    Url, \
    BrowserCantFindHistory, \
    BrowserCantFindBasePath
from browsers.history.sqlite import SQLiteHistory
from time import time


class ChromeBrowser(Browser):

    name = 'Google Chrome'
    request_headers = {}
    user_agent = None
    _base_path = ''
    _possible_paths = (
        os.path.expanduser('~/.config/google-chrome/'),
        os.path.expanduser('~/.config/chromium/'),
        'C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\' % os.environ.get('USERNAME'),
        'C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data' % os.environ.get('USERNAME'),
        'C:\\Documents and Settings\\%s\\Local Settings\\Application Data\\Google\\Chrome\\' % os.environ.get(
            'USERNAME')
    )
    _history_path = ''
    _history_db = None

    def __init__(self, browser=None):
        super().__init__(browser)
        self.user_agent = self._user_agents.chrome
        self._load_data()

    @staticmethod
    def _get_history_file(path):
        possible_path = os.path.join(path, 'Default', 'History')
        if os.path.exists(possible_path):
            return possible_path
        possible_path = os.path.join(path, 'User Data', 'Default', 'History')
        if os.path.exists(possible_path):
            return possible_path
        raise FileNotFoundError('_get_history_file::Application: cant find history')

    def _load_data(self):
        for path in self._possible_paths:
            if os.path.exists(path):
                self._base_path = path
                history_path = self._get_history_file(path)
                print(history_path)
                if os.path.exists(history_path):
                    self._history_path = history_path
                    self._history_db = SQLiteHistory(self._history_path, delete_db_copy=True)
                else:
                    raise BrowserCantFindHistory(self.name)
                break
        else:
            raise BrowserCantFindBasePath(self.name)

    def get_history(self, period=None, limit=None, order_by=None):
        sql = 'SELECT u.url FROM urls u WHERE 1'
        args = []
        if period is not None:
            if 'from' in period:
                sql += ' AND u.last_visit_time >= ?'
                args.append(int(period['from']))
            if 'to' in period:
                sql += ' AND u.last_visit_time <= ?'
                args.append(int(period['to']))
        if order_by is not None:
            sql += ' ORDER BY ' + ' '.join(order_by)
        if limit is not None:
            if 'count' in limit:
                sql += ' LIMIT ?'
                args.append(int(limit['count']))
            if 'offset' in limit:
                sql += 'OFFSET ?'
                args.append(int(limit['offset']))

        result = self._history_db.cursor.execute(sql, tuple(args))
        while True:
            r = result.fetchone()
            if r is None:
                break
            yield Url(r[0], **{'User-Agent': self.user_agent})




