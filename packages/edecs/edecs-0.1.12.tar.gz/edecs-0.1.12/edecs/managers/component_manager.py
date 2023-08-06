from ..models import (ComponentHasNoEntity, ComponentAlreadyHaveEntity,
                      EntityAlredyHaveComponent)


class ComponentManager():
    '''Component manager'''

    @property
    def components(self):
        return self._components

    @property
    def component_types(self):
        return self._component_types


    def __init__(self):
        self._component_count = 0
        self._components = []
        self._component_types = {}

    def create_component(self, component):
        if component in self._components:
            # TO DO: fix this error
            raise ComponentAlreadyHaveEntity(component)

        component._id = self._component_count
        self._component_count+=1

        self._components.append(component)

        if self._component_types.get(component.type) is None:
            self._component_types[component.type] = {}

        if self._component_types[component.type].get(component.entity.id) \
                                                                    is not None:
            EntityAlredyHaveComponent(component.entity, component)

        self._component_types[component.type][component.entity.id] = component

    def destroy_component(self, component):
        if component not in self._components:
            raise ComponentHasNoEntity(component)

        self._components[component.id] = None

        del self._component_types[component.type][component.entity.id]
        if self._component_types[component.type] == {}:
            del self._component_types[component.type]

        component._entity = None

    def component_exists(self, component_type, entity_id):
        component_types = self.component_types.get(component_type)
        if component_types is None:
            return False
        else:
            component = component_types.get(entity_id)
            return component is not None
