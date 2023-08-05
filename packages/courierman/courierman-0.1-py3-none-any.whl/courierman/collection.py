from courierman.postman_entry import PostmanEntry


class Collection(PostmanEntry):
    def __init__(self, *args, **kwargs):
        super(Collection, self).__init__(*args, **kwargs)
        self._requests = None

    @property
    def name(self):
        return self._json["info"]["name"]

    @property
    def requests(self):
        from courierman.request import Request
        from courierman.folder import Folder
        if self._requests is None:
            self._requests = []
            for item in self.items:
                if isinstance(item, Folder):
                    self._requests += item.requests
                elif isinstance(item, Request):
                    self._requests.append(item)
        return self._requests
