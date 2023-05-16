from enum import Enum
from game_engine_tools import get_asset_path


class ConstructType(Enum):
    FAMILY_HOUSE = {
        'likeness': ['home'],
        'cost': 1000,
        'zone': 'residential',
        'level': {
            0: {
                'name': 'small house',
                'people_involved': 5,  # in people
                'base_resident_satisfaction': 0.45,  # in percentage
                'energy_change': -3,  # in units 
                'water_consumption': 3,  # in units (UNIFY)
                'waste_change': 3,  # in units 
                'taxation': 1200,  # in dollars; per person; multiply by satisfaction to get actual income
                'images': [get_asset_path('House', 'Hs01.png'), get_asset_path('House', 'Hs02.png'),
                           get_asset_path('House', 'Hs03.png'),
                           get_asset_path('House', 'Hs00.png')]
            },
            1: {
                'name': 'family house',
                'people_involved': 8,
                'base_resident_satisfaction': 0.55,
                'energy_change': -6,
                'water_consumption': 5,
                'waste_change': 5,
                'taxation': 1800,
                'upgrade_cost': 800,
                'images': [get_asset_path('House', 'H05.png')]
            },
            2: {
                'name': 'large residence',
                'people_involved': 10,
                'base_resident_satisfaction': 0.65,
                'energy_change': -10,
                'water_consumption': 10,
                'waste_change': 8,
                'taxation': 2300,
                'upgrade_cost': 1000,
                'images': [get_asset_path('House', 'H04.png'), get_asset_path('House', 'H06.png')]
            }
        }
    }

    SHOP = {
        'cost': 1000,
        'zone': 'service',
        'level': {
            0: {
                'name': 'small shop',
                'people_involved': 3,
                'income': 700,
                'demand': 5,
                'energy_change': -10,
                'water_consumption': 5,
                'waste_change': 20,
                'resident_satisfaction_multiplier': 1.1,
                'images': [get_asset_path('Shop', 'SH0.png'), get_asset_path('Shop', 'SH1.png'),
                           get_asset_path('Shop', 'SH2.png')]
            },
            1: {
                'name': 'small shop',
                'people_involved': 3,
                'income': 700,
                'demand': 5,
                'energy_change': -10,
                'water_consumption': 5,
                'waste_change': 20,
                'upgrade_cost': 2000,
                'resident_satisfaction_multiplier': 1.1,
                'images': [get_asset_path('Shop', 'SH0.png'), get_asset_path('Shop', 'SH1.png'),
                           get_asset_path('Shop', 'SH2.png')]
            },
            2: {
                'name': 'shop',
                'description': 'Larger shop, meant to sustain a larger neighbourhood, be it of houses of city blocks.',
                'people_involved': 10,
                'income': 1700,
                'demand': 10,
                'energy_change': -20,
                'water_consumption': 10,
                'waste_change': 40,
                'resident_satisfaction_multiplier': 1.2,
                'upgrade_cost': 2000,
                'images': [get_asset_path('Shop', 'SH3.png')]
            }
        }
    }

    FACTORY = {
        'cost': 1000,
        'zone': 'industrial',
        'level': {
            0: {
                'name': 'factory',
                'people_involved': 50,
                'income': -1250,
                'produce': 25,
                'energy_change': -100,
                'water_consumption': 20,
                'waste_change': 70,
                'resident_satisfaction_multiplier': 0.35,
                'pollution': 0.6,
                'temperature_raise': 4,
                'images': [get_asset_path('Factory', 'factory-s-1.png'), get_asset_path('Factory', 'factory-s-2.png')]
            }
        }
    }

    STADIUM = {
        'cost': 1000,
        'level': {
            0: {
                'name': 'clinic',
                'description': 'Small clinic.',
                'people_involved': 10,
                'income': -450,
                'energy_change': -50,
                'water_consumption': 30,
                'waste_change': 100,
                'resident_satisfaction_multiplier': 1.6,
                'range': 10,
                'images': [get_asset_path('SpecialBuildings', 'hospital.png')]
            },
            1: {
                'name': 'hospital',
                'description': 'Small hospital. Can house more people.',
                'people_involved': 200,
                'income': -4500,
                'energy_change': -500,
                'water_consumption': 300,
                'waste_change': 1000,
                'resident_satisfaction_multiplier': 1.9,
                'upgrade_cost': 10000,
                'range': 18,
                'images': [get_asset_path('SpecialBuildings', 'hospital.png')]
            }
        }
    }

    POLICE_STATION = {
        'cost': 1000,
        'level': {
            0: {
                'name': 'Police outpost.',
                'description': 'Smaller scale police outpost.',
                'people_involved': 5,
                'income': 250,
                'energy_change': -10,
                'water_consumption': 5,
                'waste_change': 5,
                'resident_satisfaction_multiplier': 1.7,
                'range': 8,
                'fire_protection': 1,
                'security': 5,
                'images': [get_asset_path('SpecialBuildings', 'police0.png')]
            },
            1: {
                'name': 'Police station',
                'description': 'Local police headquarters.',
                'people_involved': 20,
                'income': 550,
                'energy_change': -50,
                'water_consumption': 20,
                'waste_change': 20,
                'resident_satisfaction_multiplier': 1.8,
                'range': 15,
                'upgrade_cost': 10000,
                'fire_protection': 2,
                'security': 10,
                'images': [get_asset_path('SpecialBuildings', 'police1.png')]
            }
        }
    }


def get_zone_construct_type(zone_type):
    if zone_type == 'residential':
        return ConstructType.FAMILY_HOUSE
    if zone_type == 'service':
        return ConstructType.SHOP
    if zone_type == 'industrial':
        return ConstructType.FACTORY
