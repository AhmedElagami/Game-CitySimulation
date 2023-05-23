import sys
import os

# Get the parent directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to the system path
sys.path.append(parent_dir)

import unittest
from constructs.building import *
from constructs.buildingType import *


class BuildingTestCase(unittest.TestCase):

    def setUp(self):
        self.building_type = BuildingType.FAMILY_HOUSE

    def test_building_initialization(self):
        building = Building(self.building_type)
        self.assertEqual(building.construct_level, 0)
        self.assertEqual(building.type_name, 'FAMILY_HOUSE')
        self.assertEqual(building.type, BuildingType.FAMILY_HOUSE.value)
        self.assertIsNotNone(building.satisfaction)
        self.assertFalse(building.heat)
        self.assertEqual(building.crime_level, 0)
        self.assertEqual(building.waste, 0)
        self.assertEqual(len(building.past_images), 1)
        self.assertIsNotNone(building.image)
        self.assertIsNotNone(building.image_path)

    def test_building_level_up(self):
        building = Building(self.building_type)
        level_up_by = 1
        level_difference = building.level_up(level_up_by)
        self.assertEqual(building.construct_level, level_up_by)
        self.assertEqual(level_difference, level_up_by)
        self.assertEqual(len(building.past_images), level_up_by + 1)
        self.assertIsNotNone(building.image)
        self.assertIsNotNone(building.image_path)

    def test_building_level_up_max_level(self):
        building = Building(self.building_type)
        max_level = len(building.type['level']) - 1
        building.construct_level = max_level
        level_difference = building.level_up()
        self.assertEqual(building.construct_level, max_level)
        self.assertEqual(level_difference, 0)
        self.assertEqual(len(building.past_images), max_level -1)
        self.assertIsNotNone(building.image)
        self.assertIsNotNone(building.image_path)

    def test_building_level_down(self):
        building = Building(self.building_type)
        building.level_up(2)
        level_down_by = 1
        level_difference = building.level_down(level_down_by)
        self.assertEqual(building.construct_level, 1)
        self.assertEqual(level_difference, level_down_by)
        self.assertIsNotNone(building.image)
        self.assertIsNotNone(building.image_path)

    def test_building_level_down_min_level(self):
        building = Building(self.building_type)
        level_difference = building.level_down()
        self.assertEqual(building.construct_level, 0)
        self.assertEqual(level_difference, 0)
        self.assertEqual(len(building.past_images), 1)
        self.assertIsNotNone(building.image)
        self.assertIsNotNone(building.image_path)

    def test_building_get_existing_key(self):
        building = Building(self.building_type)
        key = 'name'
        expected_value = self.building_type.value['level'][0]['name']
        value = building.get(key, None)
        self.assertEqual(value, expected_value)

    def test_building_get_nonexistent_key(self):
        building = Building(self.building_type)
        key = 'nonexistent_key'
        expected_value = 'default_value'
        value = building.get(key, expected_value)
        self.assertEqual(value, expected_value)

    def test_building_likes_true(self):
        building = Building(self.building_type)
        cmp_likeness = 'home'
        result = building.likes(cmp_likeness)
        self.assertTrue(result)

    def test_building_likes_false(self):
        building = Building(self.building_type)
        cmp_likeness = 'office'
        result = building.likes(cmp_likeness)
        self.assertFalse(result)

    def test_building_multiply_satisfaction(self):
        building = Building(self.building_type)
        by = 2
        building.multiply_satisfaction(by)
        self.assertIsNotNone(building.satisfaction)
        self.assertEqual(building.satisfaction, by * self.building_type.value['level'][0]['base_resident_satisfaction'])

    def test_building_compress2save(self):
        building = Building(self.building_type)
        compress_data = building.compress2save()
        self.assertIsNotNone(compress_data)
        self.assertIsInstance(compress_data, dict)
        self.assertEqual(len(compress_data), 7)
        self.assertEqual(compress_data['construct_level'], 0)
        self.assertEqual(compress_data['type'], 'FAMILY_HOUSE')
        self.assertEqual(compress_data['satisfaction'], building.satisfaction)
        self.assertEqual(compress_data['heat'], building.heat)
        self.assertEqual(compress_data['crime_level'], building.crime_level)
        self.assertEqual(compress_data['waste'], building.waste)
        self.assertEqual(compress_data['images'], building.past_images)


if __name__ == '__main__':
    unittest.main()
