from tests.game_test import *
from tests.graph_test import *
from tests.city_test import *
from tests.building_test import *
from tests.tracker_test import *
import unittest

if __name__ == "__main__":
	loader = unittest.TestLoader()
	suite = unittest.TestSuite()
	suite.addTests(loader.loadTestsFromTestCase(RoadNetGraphTestCase))
	suite.addTests(loader.loadTestsFromTestCase(SaveManagerTest))
	suite.addTests(loader.loadTestsFromTestCase(RoadSystemTest))
	suite.addTests(loader.loadTestsFromTestCase(FieldTest))
	suite.addTests(loader.loadTestsFromTestCase(BuildingTestCase))
	suite.addTests(loader.loadTestsFromTestCase(TestPlayerStatus))
	result = unittest.TextTestRunner().run(suite)

