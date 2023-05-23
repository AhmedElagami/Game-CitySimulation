from random import randint, random

import numpy as np


def set_between(value, min_value, max_value):
    if max_value is None:
        max_value = value
    if min_value is None:
        min_value = value
    return max(min_value, min(max_value, value))



def calculate_income(construct, player_status):
    income = construct.get('income', 0)
    if income > 0:
        income /= 1 + np.abs(player_status.data['goods'] - player_status.data['population'] * GOODS_PER_PERSON) / max(
            player_status.data['population'] * GOODS_PER_PERSON, 1)
    return income

def security(field, player_status):
    if field.construct is not None:
        security = 0
        coefficient = field.construct.get('burglary_appeal', 0.5)
        coefficient *= 1 if field.construct.satisfaction is None else field.construct.satisfaction
        crime_appeal = BURGLARY_APPEAL * coefficient
        for affected_by in field.affected_by:
            security += affected_by.get('security', 0.05)
        security += field.construct.get('security', 0.05)
        field.construct.crime_level += crime_appeal - security
        field.construct.crime_level = set_between(
            field.construct.crime_level, MIN_CRIME, MAX_CRIME)

# def economy_change(field, player_status):
#     if field.construct is not None:
#         money_change = field.construct.get('taxation', 0)
#         taxes_multiplier = min(field.construct.satisfaction / satisfaction_FOR_FULL_TAXES,
#                                1) if not field.construct['satisfaction'] is None else 1
#         money_change *= (1 + player_status.data['taxation']) * taxes_multiplier
#         money_change += calculate_income(field.construct, player_status)
#         player_status.data['funds'] += int(money_change)
#         player_status.data['funds'] = set_between(
#             player_status.data['funds'], MIN_MONEY, MAX_MONEY)



def produce(field, player_status):
    if field.construct is not None:
        player_status.data['produce'] += field.construct.get('produce', 0)


def demand(field, player_status):
    if field.construct is not None:
        player_status.data['demand'] += field.construct.get('demand', 0)


def population(field, player_status):
    if field.construct is not None:
        capacity = player_status.data['capacity']
        populus = player_status.data['population']
        satisfaction = player_status.data['resident_satisfaction']
        if populus < capacity and random() < POPULATION_satisfaction_COEF * satisfaction:
            populus = randint(populus, int(set_between(
                capacity * POPULATION_satisfaction_COEF * satisfaction,
                (populus + capacity) // 2,
                capacity
            ))
                              )
            player_status.data['population'] = populus
        if random() > satisfaction:
            player_status.data['population'] = int(
                player_status.data['population'] * POPULATION_REDUCTION)



def satisfy_demand(player_status):
    normalize = min(player_status.data['produce'],
                    player_status.data['demand'])
    player_status.data['goods'] = max(0,
                                      player_status.data['goods'] - player_status.data['population'] * GOODS_PER_PERSON)
    player_status.data['goods'] += int(normalize * PRODUCE_TO_GOODS)
    player_status.data['produce'] -= normalize
    player_status.data['demand'] -= normalize


def calculate_demands(player_status):
    player_status.data['service demand'] = level_to_demand(
        player_status.data['produce'] + max(0, player_status.data['population'] * GOODS_PER_PERSON - player_status.data[
            'goods']) / PRODUCE_TO_GOODS, PRODUCE_THRESHOLDS)
    player_status.data['industrial demand'] = level_to_demand(
        player_status.data['demand'], DEMAND_THRESHOLDS)
    player_status.data['residential demand'] = 'Very high' if top_demand(player_status) else level_to_demand(
        player_status.data['goods'] - player_status.data['population'] * GOODS_PER_PERSON, GOODS_THRESHOLDS)


def calculate_satisfaction(field):
    return 0 if field.construct is None or field.construct.satisfaction is None else field.construct.satisfaction


def level_to_demand(value, threshold):
    for i in range(len(DEMAND_LEVEL)):
        if value <= threshold * i or i == len(DEMAND_LEVEL) - 1:
            return DEMAND_LEVEL[i]


def top_demand(player_status):
    top_demands = DEMAND_LEVEL[-2:]
    return player_status.data['service demand'] in top_demands and player_status.data[
        'industrial demand'] in top_demands


def normalize_satisfaction(satisfaction, old_satisfaction):
    satisfaction = (satisfaction * NEW_PERCENT_WEIGHT + old_satisfaction * CURRENT_PERCENT_WEIGHT) / (
            NEW_PERCENT_WEIGHT + CURRENT_PERCENT_WEIGHT)
    satisfaction = (satisfaction + 1) ** 0.25
    satisfaction = -1 / satisfaction + 1
    if satisfaction >= 0.9994:
        satisfaction = 1
    return satisfaction


# constant listing all simulation functions to be called in a complete cycle
SIMULATIONS = [
    security,
    economy_change,
    produce,
    demand,
    population,
]

# event limit
EVENTS_LIMIT = 10

# security related constants
BURGLARY_APPEAL = 0.4
MIN_CRIME = 0
MAX_CRIME = 15
CRIME_THRESHOLD = 7
# population satisfaction constants
POPULATION_satisfaction_COEF = 0.5
POPULATION_REDUCTION = 0.60
CURRENT_PERCENT_WEIGHT = 7
NEW_PERCENT_WEIGHT = 1

# satisfaction and taxes correlation constants
satisfaction_FOR_FULL_TAXES = 3
MIN_MONEY = 0
MAX_MONEY = 1e9

# bulldozing related constants
MONEY_RETURN_PERCENT = 0.78

# supply and demand balance related constants
BASE_DEMAND = 10
PRODUCE_TO_GOODS = 2
GOODS_PER_PERSON = 1
PRODUCE_THRESHOLDS = 25
DEMAND_THRESHOLDS = 45
GOODS_THRESHOLDS = 10

# demand levels in verbose
DEMAND_LEVEL = [
    'Very low',
    'Low',
    'Satisfiable',
    'Medium',
    'Medium high',
    'High',
    'Very high'
]
