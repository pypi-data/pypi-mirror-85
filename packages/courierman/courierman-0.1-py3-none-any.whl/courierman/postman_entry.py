import os
from json import load as load_json


class PostmanEntry(object):
    """
    Postman collection Json entry

    """

    def __init__(self, filename=None, json=None):
        if filename:
            assert os.path.exists(filename)
            self._json = self.load_json(filename)
        else:
            assert json is not None
            self._json = json
        self._items = None

    @property
    def items(self):
        if self._items is None:
            self._items = [self.create(json=item)
                           for item in self._json["item"]]
        return self._items

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    @classmethod
    def create(cls, filename=None, json=None):
        from courierman.collection import Collection
        from courierman.request import Request
        from courierman.folder import Folder
        if filename:
            assert json is None
            json = cls.load_json(filename)
        if "info" in json:
            return Collection(filename=filename, json=json)
        if "request" in json:
            return Request(filename=filename, json=json)
        return Folder(filename=filename, json=json)

    @staticmethod
    def load_json(filename):
        with open(filename) as f:
            return load_json(f)
