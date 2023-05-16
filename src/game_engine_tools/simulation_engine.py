from math import inf
from city_graphics.graphics import CityGraphics
from constructs.buildingType import get_zone_construct_type
from game_engine_tools.player_status_tracker import PlayerStatus
from . import make_safe_range
from .road_graph import RoadNetGraph
from .simulation_tools import MONEY_RETURN_PERCENT, SIMULATIONS, calculate_satisfaction, normalize_satisfaction, \
    satisfy_demand, calculate_demands


class SimulationEngine:
    """ class managing simulation progress, updating statistics and demand"""

    FPS_PER_CYCLE_OPTIONS = [
        inf,
        60 * 2.5,
        60 * 1.5,
        60 * 0.5
    ]
    fps_per_cycle = 60 * 2.5

    def __init__(self, city_space, save_data):
        self.player_status = PlayerStatus(save_data.get('world_state', None))
        self.city_space = city_space
        self.fps_in_cycle = 0
        self.road_graph = RoadNetGraph(self.city_space.road_system, self.city_space.fields)
        for row in self.city_space.fields:
            for field in row:
                self.integrate_construct(field, from_save=True)

    def all_fields_empty(self, fields):
        for row in fields:
            for field in row:
                if field.construct is not None:
                    return False
        return True

    def simulate_cycle(self):
        if self.fps_in_cycle >= self.fps_per_cycle:
            self.road_graph.rebuild_references()
            self.fps_in_cycle = 0
            old_satisfaction = self.player_status.data['resident_satisfaction']
            if not self.all_fields_empty(self.city_space.fields):
                self.player_status.data['resident_satisfaction'] = 0
                for row in self.city_space.fields:
                    for field in row:
                        for simulation in SIMULATIONS:
                            simulation(field, self.player_status)
                        self.player_status.data['resident_satisfaction'] += calculate_satisfaction(field)
                self.player_status.data['resident_satisfaction'] = normalize_satisfaction(
                    self.player_status.data['resident_satisfaction'], old_satisfaction)
            satisfy_demand(self.player_status)
            calculate_demands(self.player_status)
        else:
            self.fps_in_cycle += 1

    def build_building(self, field, building_type, player_pays=True):
        if player_pays:
            self.player_status.money -= building_type.value['cost']

        field.building = {
            'type': building_type,
            'level': 0
        }
    def can_buy(self, construct=None, zone=None, level=0):
        building = construct
        if building is None:
            building = get_zone_construct_type(zone)
        return self.player_status.data['funds'] >= building.value['level'][level].get('upgrade_cost',
                                                                                      building.value['cost'])

    def funds_change_by(self, construct, multiplier=1.):
        self.player_status.data['funds'] -= construct.type['cost'] * multiplier

    def integrate_construct(self, field, remove=False, from_save=False):
        construct = field.construct

        if construct is not None:
            self.road_graph.update_field(field, remove)
            self.player_status.data['residences'] += (-1 if remove else 1) if construct.likes('home') else 0
            if not from_save:
                if construct.likes('home'):
                    people_involved = construct.get('people_involved', 0)
                    self.player_status.data['capacity'] += people_involved if not remove else -people_involved
                construct_range = int(construct.get('range', 0))
                satisfaction_multiplier = float(construct.get(
                    'resident_satisfaction_multiplier', 1))

                ind = [
                    (i, row.index(field))
                    for i, row in enumerate(self.city_space.fields)
                    if field in row
                ]
                current_row, current_column = ind[0]

                row_range = make_safe_range(0, len(self.city_space.fields))
                col_range = make_safe_range(0, len(self.city_space.fields[0]))
                for row in row_range(current_row - construct_range, current_row + construct_range + 1):
                    for col in col_range(current_column - construct_range, current_column + construct_range + 1):
                        if row != current_row or col != current_column:
                            affected_field = self.city_space.fields[row][col]
                            if affected_field.construct is not None and affected_field.construct.satisfaction is not None:
                                if remove:
                                    affected_field.construct.satisfaction /= satisfaction_multiplier
                                else:
                                    affected_field.construct.satisfaction *= satisfaction_multiplier

                if remove:
                    self.funds_change_by(field.construct, -MONEY_RETURN_PERCENT)
                else:
                    self.funds_change_by(field.construct)
                    if field.construct.likes('home'):
                        for affecting_construct in list(field.affected_by):
                            field.construct.satisfaction *= affecting_construct.get(
                                'resident_satisfaction_multiplier', 1)

    def change_speed(self, ind):
        self.fps_per_cycle = self.FPS_PER_CYCLE_OPTIONS[ind]
        CityGraphics.set_speed(ind)

    def get_data(self, key):
        return self.player_status.data.get(key, None)

    def compress2save(self):
        return self.player_status.compress2save()
