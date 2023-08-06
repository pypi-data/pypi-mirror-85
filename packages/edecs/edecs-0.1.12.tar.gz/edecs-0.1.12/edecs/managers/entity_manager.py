from ..models import (EntityNotCreated, EntityAlreadyExists)


class EntityManager():
    '''Entity manager'''

    @property
    def entities(self):
        return self._entities

    @property
    def entity_types(self):
        return self._entity_types


    def __init__(self):
        self._entity_count = 0
        self._entities = []
        self._entity_types = {}

    def create_entity(self, entity):
        if entity in self._entities:
            raise EntityAlreadyExists(entity)

        entity._id = self._entity_count
        self._entity_count+=1

        self._entities.append(entity)

        if self._entity_types.get(entity.type) is None:
            self._entity_types[entity.type] = {}
        self._entity_types[entity.type][entity.id] = entity

    def destroy_entity(self, entity):
        if entity not in self._entities:
            raise EntityNotCreated(entity)

        self._entities[entity.id] = None

        del self._entity_types[entity.type][entity.id]
        if self._entity_types[entity.type] == {}:
            del self._entity_types[entity.type]

    def entity_exists(self, entity_id):
        return entity_id < len(self.entities) and self.entities[entity_id] is not None
