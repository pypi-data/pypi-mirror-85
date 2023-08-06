from ..models import (SystemNotCreated, SystemAlreadyExists)


class SystemManager():
    '''System manager'''

    @property
    def system_types(self):
        return self._system_types


    def __init__(self):
        self._system_types = {}

    def create_system(self, system):
        if system.type in self._system_types.keys():
            raise SystemAlreadyExists(system)

        self._system_types[system.type] = system

    def destroy_system(self, system):
        if system.type not in self._system_types.keys():
            raise SystemNotCreated(system)

        del self._system_types[system.type]
