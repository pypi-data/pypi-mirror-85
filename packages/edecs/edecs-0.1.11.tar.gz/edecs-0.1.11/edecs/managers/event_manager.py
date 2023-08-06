from ..models import (FunctionNotSubscribed, FunctionAlreadySubscribed)


class EventManager():
    '''Event manager'''

    @property
    def subscribers(self):
        return self._subscribers

    @property
    def events(self):
        return self._events

    @property
    def empty(self):
        return self._events == []


    def __init__(self):
        self._subscribers = {}
        self._events = []

    def subscribe(self, fn, event_type):
        if self._subscribers.get(event_type) is None:
            self._subscribers[event_type] = []

        if fn in self._subscribers[event_type]:
            raise FunctionAlreadySubscribed(fn, event_type)

        self._subscribers[event_type].append(fn)

    def unsubscribe(self, fn, event_type):
        if self._subscribers.get(event_type) is None or \
                                        fn not in self._subscribers[event_type]:
            raise FunctionNotSubscribed(fn, event_type)

        self._subscribers[event_type].remove(fn)

        if self._subscribers[event_type] == {}:
            del self._subscribers[event_type]

    def add_event(self, event):
        self._events.append(event)

    def update_events(self):
        if self._events != []:
            event = self._events.pop(0)
            subscribers = self._subscribers.get(event.type)
            if subscribers is not None:
                for subscriber in subscribers:
                    subscriber(event)
