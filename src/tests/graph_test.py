import sys
import os

# Get the parent directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to the system path
sys.path.append(parent_dir)

from city.field_type import FieldType
from constructs.buildingType import BuildingType
from city.road_system import RoadSystem
from game_engine_tools.road_graph import RoadNetGraph
from city.field import Field
import unittest
class RoadNetGraphTestCase(unittest.TestCase):
    def setUp(self):
        self.fields = [
            [Field(0, 0, FieldType.GRASS), Field(1, 0, FieldType.GRASS)],
            [Field(0, 1, FieldType.GRASS), Field(1, 1, FieldType.GRASS)]
        ]
        self.road_system = RoadSystem()
        self.road_graph = RoadNetGraph(self.road_system, self.fields)

    def test_rebuild_references(self):
        # Ensure the references are correctly rebuilt
        self.road_graph.rebuild_references()
        for row in self.fields:
            for field in row:
                self.assertEqual(len(field.affects), 0)
                self.assertEqual(len(field.affected_by), 0)

    def test_update_field(self):
        field = self.fields[0][0]
        field.set_construct(BuildingType.FAMILY_HOUSE)
        self.road_graph.update_field(field)

        # Ensure the field and its neighbors are correctly affected
        self.assertEqual(len(field.affects), 0)
        self.assertEqual(len(field.affected_by), 0)

        # Ensure removing the construct updates the field and its neighbors
        field.remove_construct()
        self.assertEqual(len(field.affects), 0)
        self.assertEqual(len(field.affected_by), 0)



#if __name__ == '__main__':
 #   unittest.main()
