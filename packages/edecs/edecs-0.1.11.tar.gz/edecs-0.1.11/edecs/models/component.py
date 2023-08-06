import json
from .exceptions import (ComponentHasNoEntity, ComponentAlreadyHaveEntity)

class Component():
    '''Base component class'''

    #__slots__ = ['_type', '_entity']

    default_component_type = None
    defaults = {}


    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id

    @property
    def entity(self):
        return self._entity

    @property
    def initialized(self):
        return self._entity


    def __init__(self, component_type=None, **properties):
        self._type = component_type or self.default_component_type or \
                                                            type(self).__name__
        self._id = 'no_id'
        self._entity = None

        if self.defaults == {}:
            for key, value in properties.items():
                #setattr(self, key, value)
                self.defaults[key] = value

        for key, value in self.defaults.items():
            setattr(self, key, properties.pop(key, value))

    def __repr__(self):
        # <Component:type; Enity:entity>
        return "<Component:{}; Entity:{}>".format(self._type,
                                            self._entity if self._entity is None
                                                        else self._entity.type)

    def __str__(self):
        # JSON
        keys = self.defaults.keys()
        data = {}

        for key in keys:
            data[key] = getattr(self, key)

        json_string = json.dumps(data, indent=4)
        return json_string


    def create(self, entity):
        if self.initialized:
            raise ComponentAlreadyHaveEntity(self)

        self._entity = entity

    def destroy(self):
        if not self.initialized:
            raise ComponentHasNoEntity(self)

        entity = self._entity
        if entity.initialized:
            entity._component_manager.destroy_component(self)
        else:
            self._entity = None
