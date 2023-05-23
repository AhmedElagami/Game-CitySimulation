import sys
import os

# Get the parent directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to the system path
sys.path.append(parent_dir)
import unittest
from game_engine_tools.player_status_tracker import PlayerStatus

class TestPlayerStatus(unittest.TestCase):
    def test_init_with_save_source(self):
        save_source = {
            'funds': 5000,
            'population': 50,
            'capacity': 100,
            'work places': 30,
            'produce': 200,
            'demand': 150,
            'goods': 100,
            'health': 80,
            'resident_satisfaction': 0.9,
            'power': 50,
            'water': 50,
            'waste': 30,
            'pollution': 20,
            'taxation': 0.15,
            'residences': 40,
            'residential demand': 'High',
            'commercial demand': 'Low',
            'industrial demand': 'Low'
        }
        player_status = PlayerStatus(save_source)
        self.assertEqual(player_status.data, save_source)

    def test_init_without_save_source(self):
        player_status = PlayerStatus()
        expected_data = {
            'funds': 10000,
            'population': 100,
            'capacity': 0,
            'work places': 0,
            'produce': 0,
            'demand': 0,
            'goods': 0,
            'health': 0,
            'resident_satisfaction': 1,
            'power': 0,
            'water': 0,
            'waste': 0,
            'pollution': 0,
            'taxation': 0.1,
            'residences': 0,
            'residential demand': 'Very high',
            'commercial demand': 'Very low',
            'industrial demand': 'Very low'
        }
        self.assertEqual(player_status.data, expected_data)

    def test_density(self):
        player_status = PlayerStatus()
        player_status.data['population'] = 200
        player_status.data['capacity'] = 99
        self.assertAlmostEqual(player_status.density(), 2.0)

    def test_compress2save(self):
        player_status = PlayerStatus()
        expected_data = {
            'funds': 10000,
            'population': 100,
            'capacity': 0,
            'work places': 0,
            'produce': 0,
            'demand': 0,
            'goods': 0,
            'health': 0,
            'resident_satisfaction': 1,
            'power': 0,
            'water': 0,
            'waste': 0,
            'pollution': 0,
            'taxation': 0.1,
            'residences': 0,
            'residential demand': 'Very high',
            'commercial demand': 'Very low',
            'industrial demand': 'Very low'
        }
        self.assertEqual(player_status.compress2save(), expected_data)


if __name__ == "__main__":
    unittest.main()