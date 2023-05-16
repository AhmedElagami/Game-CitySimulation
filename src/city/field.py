from random import randint

from city.field_type import FieldType
from constructs.building import Building
from constructs.buildingType import BuildingType


class Field:
    def __init__(self, x, y, type_, save_source=None):
        self.type = type_

        # position info
        self.x = x
        self.y = y

        self.seed = randint(0, 5000)  # used for random image assignment

        # construct info
        self.zone_type = None
        self.construct = None
        self.construct_level = 0

        # special buildings access info
        self.affected_by = set()
        self.affects = set()
        self.unpolluted = 1

        # events (ex. fires)
        self.current_events = []

        # reading from save file
        if save_source is not None:
            self.type = FieldType(save_source['type_value'])
            self.zone_type = save_source['zone_type']
            self.seed = save_source['seed']
            if not save_source['construct'] is None:
                self.construct = Building(construct_state=save_source['construct'])
                self.construct_level = save_source.get('construct_level', 0)

    def set_zone(self, zone_type):
        """
            sets zone type as well as a construct according to it
            returns True if could place the building, False otherwise
        """
        if not self.can_place(BuildingType.FAMILY_HOUSE):
            return False

        self.zone_type = zone_type
        if zone_type == 'residential':
            self.construct = Building(BuildingType.FAMILY_HOUSE)
        elif zone_type == 'service':
            self.construct = Building(BuildingType.SHOP)
        elif zone_type == 'industrial':
            self.construct = Building(BuildingType.FACTORY)
        return True

    def set_construct(self, BuildingType):
        """
            sets bought construct with specified type if field available
            returns True if could place the building, False otherwise
        """
        if not self.can_place(BuildingType):
            return False
        self.construct = Building(BuildingType)
        self.zone_type = None
        return True

    def remove_construct(self):
        """
            used as to bulldoze the construct on this field
            returns True if there is anything to remove
        """
        if self.construct is None:
            return False

        self.construct = None
        self.construct_level = 0
        self.current_events = []
        self.zone_type = None
        return True

    def can_place(self, BuildingType):
        """returns True if a construct can be placed on currently highlighted field"""
        construct = Building(BuildingType=BuildingType)
        type = FieldType.GRASS
        if construct.likes('water'):
            type = FieldType.WATER

        return self.construct is None and self.type == type

    def compress2save(self):
        return {
            'seed': self.seed,
            'type_value': self.type.value,
            'construct': None if self.construct is None else self.construct.compress2save(),
            'construct_level': self.construct_level,
            'zone_type': self.zone_type,
            'unpolluted': self.unpolluted
        }
