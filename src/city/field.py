from random import randint

from city.field_type import FieldType
from constructs.construct import Construct
from constructs.construct_type import ConstructType

class Field:
    """
    This Field represents the grid unit of the game
    it has a type
    it has positions x and y
    a seed for assigning random images to the fields
    a zoneType: in what kind of zone is this field
    current_event: in case of a disaster, this is its flag
    """
    def __init__(self, x, y, fieldType, save_source=None):
        self.type = fieldType

        self.x = x
        self.y = y

        self.seed = randint(0, 5000)  # used for random image assignment
        # TODO why is this here?

        # construct info
        self.zoneType = None
        self.construct = None
        self.construct_level = 0
        # TODO why is this here?
        # TODO why is this here?

        # special buildings access info
        self.affected_by = set()
        self.affects = set()
        self.unpolluted = 1
        # TODO why is this here?
        # TODO why is this here?

        # events (ex. fires)
        self.current_events = []

        # reading from save file
        if save_source is not None:
            self.type = FieldType(save_source['type_value'])
            self.zone_type = save_source['zone_type']
            self.seed = save_source['seed']
            if not save_source['construct'] is None:
                self.construct = Construct(construct_state=save_source['construct'])
                self.construct_level = save_source.get('construct_level', 0)

    def assignZone(self, zone_type):
        """
            sets zone type as well as a construct according to it
            returns True if could place the building, False otherwise
        """
        if not self.canBuild(ConstructType.FAMILY_HOUSE):
            return False

        self.zone_type = zone_type
        if zone_type == 'residential':
            self.construct = Construct(ConstructType.FAMILY_HOUSE)
        elif zone_type == 'commercial':
            self.construct = Construct(ConstructType.SHOP)
        elif zone_type == 'industrial':
            self.construct = Construct(ConstructType.FACTORY)
        return True

    def build(self, construct_type):
        """
            builds a construction with specified type if the field is available
            returns True if it is built, False otherwise
        """
        if not self.canBuild(construct_type):
            return False
        self.construct = Construct(construct_type)
        self.zone_type = None
        return True

    def demolish(self):
        """
            demolishes the Field
            returns True if there is anything to remove
        """
        if self.construct is None:
            return False

        self.construct = None
        self.construct_level = 0
        self.current_events = []
        self.zone_type = None
        return True

    def canBuild(self, construct_type):
        """returns True if a construction can be built on the currently hovered Field"""
        construct = Construct(construct_type=construct_type)
        self.type = FieldType.GRASS
        if construct.likes('water'):
            self.type = FieldType.WATER

        return self.construct is None and self.type == type

    def getFields(self):
        return {
            'seed': self.seed,
            'type_value': self.type.value,
            'construct': None if self.construct is None else self.construct.compress2save(),
            'construct_level': self.construct_level,
            'zone_type': self.zone_type,
            'unpolluted': self.unpolluted
        }
