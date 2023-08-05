from courierman.collection import Collection


class Folder(Collection):
    @property
    def name(self):
        return self._json["name"]
