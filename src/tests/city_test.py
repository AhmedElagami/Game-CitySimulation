import sys
import os

# Get the parent directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to the system path
sys.path.append(parent_dir)

# Import module2
# from city import road_system

import unittest
from city import VERTICAL, HORIZONTAL
from city.road_system import RoadSystem
from random import seed
from city.field_type import FieldType
from constructs.building import Building
from constructs.buildingType import BuildingType
from city.field import Field


class FieldTest(unittest.TestCase):
    def setUp(self):
        seed(123)  # Set a fixed seed for predictable test results

    def test_set_zone(self):
        field = Field(0, 0, FieldType.GRASS)
        self.assertTrue(field.set_zone('residential'))
        self.assertEqual(field.zone_type, 'residential')

    def test_set_construct(self):
        field = Field(0, 0, FieldType.GRASS)
        self.assertTrue(field.set_construct(BuildingType.SHOP))
        self.assertEqual(field.construct.type_name, "SHOP")

    def test_remove_construct(self):
        field = Field(0, 0, FieldType.GRASS)
        field.set_construct(BuildingType.SHOP)
        self.assertTrue(field.remove_construct())
        self.assertIsNone(field.construct)

    def test_can_place(self):
        field = Field(0, 0, FieldType.GRASS)
        self.assertTrue(field.can_place(BuildingType.FAMILY_HOUSE))
        self.assertTrue(field.can_place(BuildingType.FACTORY))

        field.set_construct(BuildingType.SHOP)
        self.assertFalse(field.can_place(BuildingType.SHOP))

    def test_compress2save(self):
        field = Field(0, 0, FieldType.GRASS)
        field.set_construct(BuildingType.FAMILY_HOUSE)
        field.construct_level = 2
        field.zone_type = 'residential'
        field.unpolluted = 0.8

        save_data = field.compress2save()
        self.assertEqual(save_data['seed'], 428)
        self.assertEqual(save_data['type_value'], FieldType.GRASS.value)
        self.assertIsNotNone(save_data['construct'])
        self.assertEqual(save_data['construct_level'], 2)
        self.assertEqual(save_data['zone_type'], 'residential')
        self.assertEqual(save_data['unpolluted'], 0.8)

    def test_init_with_save_source(self):
        save_data = {
            'seed': 456,
            'type_value': FieldType.WATER.WATER,
            'construct': Building(BuildingType.SHOP).compress2save(),
            'construct_level': 1,
            'zone_type': 'service',
            'unpolluted': 1
        }

        field = Field(0, 0, FieldType.GRASS, save_source=save_data)

        self.assertEqual(field.seed, 456)
        self.assertEqual(field.type, FieldType.WATER)
        self.assertIsNotNone(field.construct)
        self.assertEqual(field.construct_level, 1)
        self.assertEqual(field.zone_type, 'service')
        self.assertEqual(field.unpolluted, 1)


class RoadSystemTest(unittest.TestCase):
    def test_add_road(self):
        road_system = RoadSystem()
        road_system.add_road(VERTICAL, (0, 0))
        road_system.add_road(HORIZONTAL, (1, 1))

        self.assertEqual(road_system.get_road_count(), 2)
        self.assertTrue(road_system.has_road(0, 0, VERTICAL))
        self.assertTrue(road_system.has_road(1, 1, HORIZONTAL))

    def test_remove_road(self):
        road_system = RoadSystem()
        road_system.add_road(VERTICAL, (0, 0))
        road_system.add_road(HORIZONTAL, (1, 1))

        road_system.remove_road(VERTICAL, (0, 0))
        road_system.remove_road(HORIZONTAL, (1, 1))

        self.assertEqual(road_system.get_road_count(), 0)
        self.assertFalse(road_system.has_road(0, 0, VERTICAL))
        self.assertFalse(road_system.has_road(1, 1, HORIZONTAL))

    def test_hovered(self):
        road_system = RoadSystem()
        road_system.hovered((2, 3))
        self.assertEqual(road_system.hovered_road, (2, 3))
        self.assertEqual(road_system.hovered_direction, VERTICAL)

        road_system.hovered(None)
        self.assertIsNone(road_system.hovered_road)

    def test_compress2save(self):
        road_system = RoadSystem()
        road_system.add_road(VERTICAL, (0, 0))
        road_system.add_road(HORIZONTAL, (1, 1))

        save_data = road_system.compress2save()
        self.assertCountEqual(save_data['vertical'], [(0, 0)])
        self.assertCountEqual(save_data['horizontal'], [(1, 1)])

if __name__ == '__main__':
    unittest.main()
