from city.field import Field
from city.field_type import FieldType
from city.roads import Roads


class CityGrid:
    """main class representing the city"""

    def __init__(self, width, height, save_source=None, map=None):
        self.height = height  # amount of fields in height
        self.width = width  # amount of fields in width

        # roads
        self.road_system = Roads(None if save_source is None else save_source['roads'])

        # lots
        self.lots = []
        self.reloadFields(
            None if save_source is None else save_source['lots'], map)

    def reloadFields(self, save_source=None, map=None):
        """
        If no save data available - creates new lot grid.
        Else - loads lots form memory.
        """

        if save_source is None:
            if map is not None:
                self.lots = [
                    [Field(x, y, FieldType(map[x][y])) for y in range(self.height)] for x in range(self.width)
                ]

            else:
                self.lots = [
                    [Field(x, y,
                         FieldType.WATER if x == 0 or x == self.height - 1 or y == 0 or y == self.width - 1 else FieldType.GRASS)
                     for y in range(self.height)] for x in range(self.width)
                ]

        else:
            self.lots = [
                [Field(x, y, None, save_source=save_source[x][y]) for y in range(self.height)] for x in range(self.width)
            ]

    def handleRoadClicked(self):
        """informs the road system that a road was clicked"""
        self.road_system.handleRoadHovered()

    def getCity(self):
        c2s = {
            'lots': [
                [Field.getFields() for lot in row] for row in self.lots
            ],
            'roads': self.road_system.getRoads()
        }
        return c2s
