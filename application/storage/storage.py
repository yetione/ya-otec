import os
import sqlite3
import marshal
import json
from time import time
from urllib.parse import urlparse

class Storage:
    file_name = '_data.sqlite'
    file_path = './data/'
    db_path = None
    connection = None
    cursor = None

    def __init__(self, file_name=None):
        if file_name is not None:
            self.file_name = file_name
        self.get_db_path()
        self._connect()
        self.options = Options(self)
        self.urls = Urls(self)

    def __del__(self):
        self.connection.commit()
        self._disconnect()

    def _connect(self, reconnect=False):
        if self.connection is None or reconnect:
            path = self.get_db_path()
            need_install = not os.path.exists(path)
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
            if need_install:
                self._install()

    def _disconnect(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()

    def _install(self, install_script=None):
        if install_script is None:
            install_script = os.path.realpath('./application/storage/install.sql')
        if not os.path.isfile(install_script):
            raise FileNotFoundError('Application Storage: installation file not found.')
        script = open(install_script, 'r')
        self.cursor.executescript(script.read())
        self.connection.commit()
        script.close()

    def get_db_path(self, update=False):
        """
        :param update:
        :rtype string:
        :return:
        """
        if self.db_path is None or update:
            self.db_path = os.path.join(os.path.realpath(self.file_path), self.file_name)
        return self.db_path


class Options:
    _data = {}
    storage = None

    def __init__(self, storage):
        self.storage = storage

    def get(self, key, default=None):
        if key not in self._data:
            result = self.storage.cursor.execute("SELECT option_value FROM options WHERE option_key=?", (key,))
            value = result.fetchone()
            try:
                self._data[key] = default if not value else marshal.loads(value[0])
            except ValueError:
                self._data[key] = default
                print('get_option::Application Storage: error value for option ' + key)
            except EOFError:
                self._data[key] = default
                print('get_option::Application Storage: error end of file for option ' + key)
            except TypeError:
                self._data[key] = default
                print('get_option::Application Storage: type error for option ' + key)
        return self._data[key]

    def set(self, key, value):
        try:
            self.storage.cursor.execute('INSERT OR REPLACE INTO options(option_key, option_value) VALUES (?, ?)',
                                (key, marshal.dumps(value)))
            self._data[key] = value
            self.storage.connection.commit()
            return True
        except ValueError:
            print('set_option::Application Storage: cant set option value error' + key)
            return False
        except sqlite3.InternalError:
            print('set_option::Application Storage: cant set option error in DB ' + key)
            return False


class Urls:

    storage = None

    def __init__(self, storage):
        self.storage = storage

    def get(self, address=None, date_add=None, last_visit=None, request_type=None, is_active=True, limit=None):
        sql = "SELECT * FROM urls WHERE 1"
        sql_args = []
        if address is not None:
            sql += " AND address=?"
            sql_args.append(address)
        if date_add is not None and isinstance(date_add, dict):
            if 'from' in date_add:
                sql += " AND date_add>=?"
                sql_args.append(date_add['from'])
            if 'to' in date_add:
                sql += " AND date_add<=?"
                sql_args.append(date_add['to'])
        if last_visit is not None and isinstance(last_visit, dict):
            if 'from' in last_visit:
                sql += " AND last_visit>=?"
                sql_args.append(last_visit['from'])
            if 'to' in last_visit:
                sql += " AND last_visit<=?"
                sql_args.append(last_visit['to'])
        if request_type is not None:
            if isinstance(request_type, (list, tuple)):
                sql += " AND request_type IN (" + ','.join(['?' for x in range(0, len(request_type))])
                sql_args += list(request_type) if isinstance(request_type, tuple) else request_type
            elif isinstance(request_type, str):
                sql += " AND request_type=?"
                sql_args.append(request_type)
        if is_active is not None:
            sql += " AND is_active=?"
            sql_args.append(int(is_active))
        if limit is not None and isinstance(limit, dict):
            if 'count' in limit:
                sql += ' LIMIT ?'
                sql_args.append(int(limit['count']))
            if 'offset' in limit:
                sql += 'OFFSET ?'
                sql_args.append(int(limit['offset']))

        try:
            result = self.storage.cursor.execute(sql, tuple(sql_args))
            while True:
                record = result.fetchone()
                if not record:
                    break
                yield Url(self, record)
        except sqlite3.OperationalError:
            print('get::Urls Model: error when load urls')

    def save(self, url):
        if url.id is None:
            sql = "INSERT INTO urls(address, headers, cookies, date_add, last_visit, request_type, is_active, add_by) VALUES (?,?,?,?,?,?,?,?)"
            sql_args = (url.address, url.get_headers(True),
                        url.get_cookies(True), url.date_add,
                        url.last_visit, url.request_type,
                        url.is_active, url.add_by)
        else:
            sql = 'UPDATE urls SET address=?, headers=?, cookies=?, date_add=?, last_visit=?, request_type=?, is_active=?, add_by=? WHERE id=?'
            sql_args = (url.address, url.get_headers(True),
                        url.get_cookies(True), url.date_add,
                        url.last_visit, url.request_type,
                        url.is_active, url.add_by, url.id)
        try:
            self.storage.cursor.execute(sql, sql_args)
            return True
        except sqlite3.OperationalError:
            print('save::Url: cant save url ' + url.address)
            return False

    def create(self):
        """
        :rtype: Url
        :return: New Url object
        """
        return Url(self)


class Url:
    id = None
    address = None
    headers = None
    cookies = None
    date_add = None
    last_visit = None
    request_type = None
    is_active = None
    add_by = None

    _parsed = None
    _model = None

    def __init__(self, model, params=None):
        if params is None:
            params = []
        self._model = model
        if len(params) != 9 and len(params) != 0:
            raise ValueError('__init__::Url: cant init url from array of params with length ' + str(len(params)))
        self.date_add = time()
        try:
            self.init_params(params)
        except ValueError:
            pass

    def __setattr__(self, key, value):
        json_fields = ('headers', 'cookie')
        try:
            json_fields.index(key)
            if isinstance(value, str):
                value = json.loads(value)
        except json.decoder.JSONDecodeError:
            print('__setattr__::Url: cant decode header')
            value = None
        except ValueError:
            pass
        if key == 'address':
            self.__dict__['_parsed'] = urlparse(value)
        self.__dict__[key] = value

    def init_params(self, params):
        if len(params) != 9:
            raise ValueError('init_params::Url: params length must be 9. Received: ' + str(len(params)))
        self.id, self.address, self.headers, self.cookies, self.date_add, self.last_visit, self.request_type, self.is_active, self.add_by = params
        self._parsed = urlparse(self.address)

    def get_headers(self, serialize=False):
        return json.dumps(self.headers) if serialize else self.headers

    def get_cookies(self, serialize=False):
        return json.dumps(self.cookies) if serialize else self.cookies

    def get_url(self):
        return self._parsed.scheme + '://' + self._parsed.netloc + self._parsed.path

    def save(self):
        return self._model.save(self)



