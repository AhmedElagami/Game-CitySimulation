from city.field import Field
from city.field_type import FieldType
from city.road_system import RoadSystem


class City:
    """main class representing the city"""

    def __init__(self, width, height, save_source=None, map=None):
        self.height = height  # amount of fields in height
        self.width = width  # amount of fields in width

        # roads
        self.road_system = RoadSystem(None if save_source is None else save_source['roads'])

        # fields
        self.fields = []
        self.reset_fields(
            None if save_source is None else save_source['fields'], map)

    def reset_fields(self, save_source=None, map=None):
        """
        If no save data available - creates new field grid.
        Else - loads fields form memory.
        """

        if save_source is None:
            if map is not None:
                self.fields = [
                    [Field(x, y, FieldType(map[x][y])) for y in range(self.height)] for x in range(self.width)
                ]

            else:
                self.fields = [
                    [Field(x, y,
                         FieldType.WATER if x == 0 or x == self.height - 1 or y == 0 or y == self.width - 1 else FieldType.GRASS)
                     for y in range(self.height)] for x in range(self.width)
                ]

        else:
            self.fields = [
                [Field(x, y, None, save_source=save_source[x][y]) for y in range(self.height)] for x in range(self.width)
            ]

    def handle_road_clicked(self):
        """informs the road system that a road was clicked"""
        self.road_system.handle_road_clicked()

    def compress2save(self):
        c2s = {
            'fields': [
                [field.compress2save() for field in row] for row in self.fields
            ],
            'roads': self.road_system.compress2save()
        }
        return c2s
