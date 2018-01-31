import sqlite3
import os
import sqlite3
from hashlib import md5
from time import time
from shutil import copy2

from browsers.history import History
from browsers.history.errors import SQLiteFileNotFound


class SQLiteHistory(History):
    db_file = None
    copy_db = True
    copy_dir = './data/'
    delete_db_copy = True
    commit_on_destruct = True
    connection = None
    cursor = None

    def __init__(self, db_file, *args, **kwargs):
        super().__init__()
        if not os.path.exists(db_file):
            raise SQLiteFileNotFound(db_file)
        self.db_file = db_file
        self.copy_db = kwargs.get('copy_db', True)
        self.copy_dir = kwargs.get('copy_dir', './data/')
        self.delete_db_copy = kwargs.get('delete_db_copy', True)
        self.commit_on_destruct = kwargs.get('commit_on_destruct', True)
        if self.copy_db:
            self._copy_db()
        self._connect()

    def __del__(self):
        if self.commit_on_destruct:
            self.commit()
        self.close()
        if self.copy_db and self.delete_db_copy:
            if self.db_file.index(os.path.realpath(self.copy_dir)) == 0:
                os.remove(self.db_file)

    def _copy_db(self):
        db_name = os.path.basename(self.db_file)
        pos = db_name.rfind('.')
        if pos > 0:
            db_name = db_name[:pos]
        salt = md5()
        salt.update(str(time()).encode('utf-8'))
        db_name += salt.hexdigest()+'.sqlite'
        db_path = os.path.realpath(os.path.join(self.copy_dir, db_name))
        db_dirs = os.path.dirname(db_path)

        if not os.path.isdir(db_dirs):
            try:
                os.makedirs(db_dirs, 0o755)
            except OSError:
                pass
        if copy2(self.db_file, db_path) == db_path:
            self.db_file = db_path
            return True
        return False

    def _connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()











