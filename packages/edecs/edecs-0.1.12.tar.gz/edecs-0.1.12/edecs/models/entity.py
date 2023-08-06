from copy import deepcopy
from .exceptions import (EntityNotCreated, EntityAlreadyExists,
                         ComponentAlreadyHaveEntity)


class Entity():
    '''Base entity class'''

    __slots__ = ['_type', '_id', '_name', '_components',
                 '_entity_manager', '_component_manager']

    default_entity_type = None
    default_components = {}


    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def components(self):
        return self._components

    @property
    def initialized(self):
        return self._entity_manager and self._component_manager


    def __init__(self, name, entity_type=None):
        self._type = entity_type or self.default_entity_type or \
                                                            type(self).__name__

        self._id = 'no_id'
        self._name = name
        self._components = deepcopy(self.default_components)

        for component in self._components.values():
            component.create(self)

        self._entity_manager = None
        self._component_manager = None

    def __repr__(self):
        return "<Entity:{}; {}:{}>".format(self._type, self._name, self._id)

    def __str__(self):
        ent = "<Entity:{}; {}:{}>".format(self._type, self._name, self._id)
        components = self._components
        # TO DO: return repr of component
        # repr(component)
        return "{}\n{}".format(ent, components)

    def __getitem__(self, key):
        return self._components[key]

    def __setitem__(self, key, value):
        if value.initialized:
            raise ComponentAlreadyHaveEntity(value)

        old_component = self._components.pop(key, None)
        if old_component is not None:
            old_component.destroy()

        self._components[key] = value
        value.create(self)

        if self.initialized:
            self._component_manager.create_component(value)
            
    def __delitem__(self, key):
        component = self._components.pop(key)
        component.destroy()

    def __getattr__(self, key):
        if key in super().__getattribute__('__slots__'):
            return super().__getattr__(key)
        else:
            return self._components[key]

    def __setattr__(self, key, value):
        if key in super().__getattribute__('__slots__'):
            super().__setattr__(key, value)
        else:
            if value.initialized:
                raise ComponentAlreadyHaveEntity(value)

            old_component = self._components.pop(key, None)
            if old_component is not None:
                old_component.destroy()

            self._components[key] = value
            value.create(self)

            if self.initialized:
                self._component_manager.create_component(value)
                
    def __delattr__(self, key):
        component = self._components.pop(key)
        component.destroy()


    def create(self, entity_manager, component_manager):
        if self.initialized:
            raise EntityAlreadyExists(self)

        self._entity_manager = entity_manager
        self._component_manager = component_manager

        self._entity_manager.create_entity(self)
        for component in self._components.values():
            self._component_manager.create_component(component)

    def destroy(self):
        if not self.initialized:
            raise EntityNotCreated(self)

        for component in self._components.values():
            self._component_manager.destroy_component(component)
        self._entity_manager.destroy_entity(self)

        self._entity_manager = None
        self._component_manager = None
