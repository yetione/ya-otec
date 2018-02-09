import os

import sys

from browsers import Browser, BrowserCantFindHistory, BrowserCantFindBasePath, Url
from browsers.history.sqlite import SQLiteHistory


class FirefoxBrowser(Browser):

    name = 'Mozilla Firefox'
    request_headers = {}
    user_agent = None
    _base_path = ''
    _history_path = ''
    _history_db = None

    def __init__(self, browser):
        super().__init__(browser)
        self.user_agent = self._user_agents.firefox
        self._load_data()

    def _load_data(self):
        if sys.platform.startswith('win'):
            path = '\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
        elif sys.platform.startswith('linux'):
            path = "/.mozilla/firefox/"
        elif sys.platform.startswith('darwin'):
            path = '/Library/Application Support/Firefox/Profiles/'
        else:
            raise BrowserCantFindHistory(self.name)
        home_dir = os.environ['HOME']
        firefox_path = home_dir + path
        self._base_path = firefox_path

        profiles = [i for i in os.listdir(firefox_path) if i.endswith('.default')]
        history_path = firefox_path + profiles[0] + '/places.sqlite'
        if os.path.exists(history_path):
            self._history_path = history_path
            self._history_db = SQLiteHistory(self._history_path, delete_db_copy=True)
        else:
            raise BrowserCantFindHistory(self.name)

    def get_history(self, period=None, limit=None, order_by=None):
        sql = 'SELECT u.url FROM moz_places u WHERE last_visit_date IS NOT NULL '
        args = []
        if period is not None:
            if 'from' in period:
                sql += ' AND u.last_visit_date >= ?'
                args.append(int(period['from']))
            if 'to' in period:
                sql += ' AND u.last_visit_date <= ?'
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
