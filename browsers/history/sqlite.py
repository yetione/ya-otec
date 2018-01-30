import sqlite3

from browsers.history import History


class SQLiteHistory(History):

    def __init__(self, db_file, *args, **kwargs):
        super().__init__()
