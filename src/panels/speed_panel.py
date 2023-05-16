import pygame_menu as pgmen

from city_graphics.assets import Assets
from panels.panel import Panel


class SpeedPanel(Panel):
    city_images = Assets()

    def __init__(self, width, height, position, window, simulator):
        super().__init__(width, height, window)
        self.menu = pgmen.Menu(title='speed',
                               width=width, height=height,
                               position=position,
                               theme=self.get_theme(),
                               rows=2, columns=4,
                               mouse_enabled=True)
        self.simulator = simulator

        # icons
        scale = (0.06, 0.06)

        self.buttons = []
        # speed buttons
        self.buttons += [self.menu.add.button('0x', self.set_speed(0))]

        self.buttons += [self.menu.add.button('1x', self.set_speed(1))]

        self.buttons += [self.menu.add.button('2x', self.set_speed(2))]

        self.buttons += [self.menu.add.button('3x', self.set_speed(3))]

        self.buttons[1].select(update_menu=True)

    def set_speed(self, value):
        def change_simulation_speed():
            self.simulator.change_speed(value)

        return change_simulation_speed
