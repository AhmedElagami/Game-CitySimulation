import sys
import os

# Get the parent directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to the system path
sys.path.append(parent_dir)


import unittest
import json
import os
from time import gmtime, strftime
from game_engine_tools.save_manager import SaveManager


class SaveManagerTest(unittest.TestCase):
    def setUp(self):
        self.save_manager = SaveManager()
        self.save_manager.generate_save_manager_data_to('test_save_manager_data.json')

    def tearDown(self):
        os.remove('test_save_manager_data.json')

    def test_has_active_save(self):
        self.assertTrue(self.save_manager.has_active_save())

    def test_create_save(self):
        self.assertEqual(self.save_manager.create_save("Save 1"), "Save Save 1 created successfully")
        self.assertTrue(self.save_manager.has_active_save())

    def test_set_active_save(self):
        self.save_manager.create_save("Save 1")
        self.save_manager.create_save("Save 2")
        self.save_manager.set_active_save()
        self.assertIsNotNone(self.save_manager.active_save)

    def test_delete_save(self):
        self.save_manager.create_save("Save 1")
        self.save_manager.set_active_save()
        self.save_manager.delete_save()
        self.assertTrue(self.save_manager.has_active_save())

    def test_load_save(self):
        self.save_manager.create_save("Save 1")
        self.save_manager.set_active_save()
        self.save_manager.save()
        self.save_manager.load_save()
        self.assertIsNotNone(self.save_manager.active_save)

    def test_save(self):
        self.save_manager.create_save("Save 1")
        self.save_manager.set_active_save()
        game_save_data = {"score": 100, "level": 5}
        self.save_manager.save(game_save_data)
        self.assertIsNotNone(self.save_manager.active_save)

        save_id, save_name, save_data = self.save_manager.active_save
        save_path = os.path.join('SaveFiles', 'save' + str(save_id) + '.json')
        with open(save_path, 'r') as save_file:
            saved_data = json.load(save_file)

        self.assertEqual(saved_data['game_state'], game_save_data)

    def test_list_saves(self):
        self.save_manager.create_save("Save 1")
        self.save_manager.create_save("Save 2")
        self.save_manager.create_save("Save 3")

        expected_saves = [
            ('[ Save 1 ] id: 1', '1'),
            ('[ Save 2 ] id: 2', '2'),
            ('[ Save 3 ] id: 3', '3')
        ]
        saves_list = self.save_manager.list_saves()

    def test_get_gameplay_data(self):
        self.save_manager.create_save("Save 1")
        self.save_manager.set_active_save()
        game_save_data = {"score": 100, "level": 5}
        self.save_manager.save(game_save_data)

        gameplay_data = self.save_manager.get_gameplay_data()
        self.assertEqual(gameplay_data, game_save_data)


if __name__ == '__main__':
    unittest.main()
