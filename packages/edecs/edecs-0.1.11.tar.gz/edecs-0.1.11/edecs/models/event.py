class Event():
    '''Event class'''


    __slots__ = ['_type', '_data']

    default_event_type = None
    default_event_data = {}


    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data


    def __init__(self, type=None, data=None):
        self._type = type or self.default_event_type or type(self).__name__
        self._data = data or self.default_event_data

    def __repr__(self):
        # <Event:event_type>
        return "<Event:{}".format(self.type)

    def __str__(self):
        # <Event:event_type>
        # {data}
        return "<Event:{}>\n{}".format(self.type, self.data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        self._data.pop(key)

    def __getattr__(self, key):
        if key in super().__getattribute__('__slots__'):
            return super().__getattr__(key)
        else:
            return self._data[key]

    def __setattr__(self, key, value):
        if key in super().__getattribute__('__slots__'):
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def __delattr__(self, key):
        self._data.pop(key)
