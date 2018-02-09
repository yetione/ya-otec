from application.storage.storage import Storage


class BaseStorage:

    table_name = None
    storage = None

    def get_list(self):
        assert isinstance(self.storage, Storage)
        self.storage.connection