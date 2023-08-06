class EntityAlreadyExists(Exception):

    def __init__(self, entity):
        self.entity = entity

    def __str__(self):
        return "Entity {} already exist".format(self.entity)

class EntityNotCreated(Exception):

    def __init__(self, entity):
        self.entity = entity

    def __str__(self):
        return "Entity {} not created".format(self.entity)

class EntityAlredyHaveComponent(Exception):

    def __init__(self, entity, component):
        self.entity = entity
        self.component = component

    def __str__(self):
        return "Entity {} already has a component {}".format(self.entity,
                                                             self.component)

class ComponentAlreadyHaveEntity(Exception):

    def __init__(self, component):
        self.component = component

    def __str__(self):
        return "Component {} already have entity {}".format(self.component,
                                                        self.component.entity)

class ComponentHasNoEntity(Exception):

    def __init__(self, component):
        self.component = component

    def __str__(self):
        return "Component {} has no entity".format(self.component)

class SystemAlreadyExists(Exception):

    def __init__(self, system):
        self.system = system

    def __str__(self):
        return "System {} already exists".format(self.system)

class SystemNotCreated(Exception):

    def __init__(self, system):
        self.system = system

    def __str__(self):
        return "System {} not created".format(self.system)

class FunctionAlreadySubscribed(Exception):

    def __init__(self, fn, event_type):
        self.fn = fn
        self.event_type = event_type

    def __str__(self):
        return "Function {} already subscribed to the event {}".format(self.fn,
                                                                self.event_type)

class FunctionNotSubscribed(Exception):

    def __init__(self, fn, event_type):
        self.fn = fn
        self.event_type = event_type

    def __str__(self):
        return "Function {} not subscribed to the event {}".format(self.fn,
                                                                self.event_type)
