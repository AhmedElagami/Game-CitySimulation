import os
from random import random, choice, seed
from time import time_ns

import pygame as pg

from city import HORIZONTAL
from city.field_type import FieldType
from city_graphics import ROAD_WIDTH_RATIO
from game_engine_tools import load_asset, get_asset_path, Singleton


class CityImages(metaclass=Singleton):
    """scaled and original background field images"""
    current_scale = -1

    def __init__(self):
        self.main_images = {
            FieldType.GRASS: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER: load_asset('FieldType', 'PNG', 'tile.png'),

            FieldType.WATER_RIGHT: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_LEFT: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_UP: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_DOWN: load_asset('FieldType', 'PNG', 'tile.png'),

            FieldType.WATER_CORNER_LEFT_UP: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_CORNER_LEFT_DOWN: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_CORNER_RIGHT_UP: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_CORNER_RIGHT_DOWN: load_asset('FieldType', 'PNG', 'tile.png'),

            FieldType.WATER_IN_CORNER_LEFT_UP: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_IN_CORNER_LEFT_DOWN: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_IN_CORNER_RIGHT_UP: load_asset('FieldType', 'PNG', 'tile.png'),
            FieldType.WATER_IN_CORNER_RIGHT_DOWN: load_asset(
                'FieldType', 'PNG', 'tile.png')
        }

        self.additional_images = {
            FieldType.GRASS: [
                load_asset('FieldType', 'PNG', f'tile.png') for i in [155, 156, 158, 160]
            ],
            FieldType.WATER: [
                load_asset('FieldType', 'island.png')
            ]}

        # chance of adding an addition image on specific field type:
        self.frequency = {
            FieldType.GRASS: 0.1,
            FieldType.WATER: 0.005
        }

        self.icons = {
            path.name.split('.')[-2]: path.path for path in os.scandir(get_asset_path("Icons2"))
        }

        self.warning_icons = {
            path.name.split('.')[-2]: path.path for path in os.scandir(get_asset_path("WarningIcons"))
        }

        self.vertical_road = load_asset('Streets', 'vertical.png')
        self.horizontal_road = load_asset('Streets', 'horizontal.png')

        self.cars = {
            key: load_asset('Cars', f'{key}.png') for key in [
                'mini-van', 'audi', 'mini-truck', 'taxi'
            ]
        }

        self.animation_images = {
            'burglary': [load_asset('Animations', 'Roll jump', f'rj_{i:03}.png') for i in range(37)]
        }

        self.scaled_main_images = self.main_images
        self.scaled_additional_images = self.additional_images
        self.scaled_cars = self.additional_images
        self.scaled_vertical = self.vertical_road
        self.scaled_horizontal = self.horizontal_road

    def rescale(self, scale):
        if scale == self.current_scale:
            return
        self.current_scale = scale

        self.scaled_main_images = {k: pg.transform.scale(
            v, (scale, scale)) for k, v in self.main_images.items()}

        self.scaled_cars = {k: pg.transform.scale(
            v, (int(scale * ROAD_WIDTH_RATIO * 1.1), int(scale * ROAD_WIDTH_RATIO * 1.1))) for k, v in
            self.cars.items()}

        self.scaled_additional_images = {k: list(map(lambda x: pg.transform.scale(
            x, (scale, scale)), v)) for k, v in self.additional_images.items()}

        self.scaled_vertical = pg.transform.scale(self.vertical_road, (int(scale * ROAD_WIDTH_RATIO), int(scale + scale * ROAD_WIDTH_RATIO)))
        self.scaled_horizontal = pg.transform.scale(self.horizontal_road, (int(scale + scale * ROAD_WIDTH_RATIO), int(scale * ROAD_WIDTH_RATIO)))

    def get_images(self, field_type, field_seed):
        seed(field_seed)
        images = [self.scaled_main_images[field_type]]
        if field_type in self.scaled_additional_images and random() < self.frequency[field_type]:
            images += [choice(self.scaled_additional_images[field_type])]
        return images

    def get_icon(self, icon):
        return self.icons[icon]

    def get_warning_icon(self, icon):
        return self.warning_icons[icon]

    def get_scaled_car_image(self, car_type, road_direction, direction):
        image = self.scaled_cars[car_type]
        if road_direction == HORIZONTAL:
            image = pg.transform.rotate(image, -direction * 90)
        return image

    def get_random_car_type(self):
        seed(time_ns())
        return choice(list(self.cars.keys()))

    def get_animation_image(self, animation_type, frame, size):
        image = self.animation_images[animation_type][frame % len(
            self.animation_images[animation_type])]
        return pg.transform.scale(image, (size, size))
