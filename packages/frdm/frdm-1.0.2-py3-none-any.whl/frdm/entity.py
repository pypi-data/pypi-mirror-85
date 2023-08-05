from .api_call import api_call


class Entity(object):
    """Base entity abstraction with common methods to update and push data the the API
    """

    def __init__(self, _id, _data):
        self._id = _id
        self._data = _data
        if _data is None:
            self.update()

    def _make_url(self):
        """Makes the base url for each entity and uses it for api requests.
        Needs to be overwritten on each subclass
        """
        raise NotImplementedError()

    def __setitem__(self, key, value):
        self._data[key] = value

    def push(self, data=None):
        """Push current data to the API. For updating only specific fields, use data argument.
        """
        if data is None:
            data = self._data
        api_call("PUT", self._make_url(), data=data)

    def update(self):
        """Synchronizes device properties with the Freedom API server.
        """
        self._data = api_call("GET", self._make_url())

    def __repr__(self):
        return "<{}: {} {}>".format(
            self.__class__.__name__,
            self._id,
            self._data.get("name", "")
        )

    def __eq__(self, obj):
        return isinstance(obj, self.__class__) and obj._id == self._id
