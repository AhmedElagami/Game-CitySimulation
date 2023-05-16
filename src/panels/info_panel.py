import pygame_menu as pgmen

from city_graphics.city_images import CityImages
from panels.panel import Panel


class InfoPanel(Panel):
    def __init__(self, width, height, position, game_window, simulator):
        super().__init__(width, height, game_window)

        self.simulator = simulator

        # menu
        self.menu = pgmen.Menu('your city: ', width=width,
                               height=height, position=position,
                               theme=self.get_theme(), columns=2, rows=12)

        # info
        funds_label = self.menu.add.label('money')
        satisfaction_label = self.menu.add.label('satisfaction')
        population_label = self.menu.add.label('population')

        funds_label.add_draw_callback(self.update_label('funds'))
        population_label.add_draw_callback(self.update_label('population'))
        satisfaction_label.add_draw_callback(
            self.update_label('resident_satisfaction'))

        self.labels = [funds_label, satisfaction_label, population_label]

    def update_label(self, key):
        def update(widget, menu):
            text = widget.get_title().split(':')[0]
            value = self.simulator.get_data(key)

            if text.strip() == 'satisfaction':
                widget.set_title(
                    f'satisfaction: {value:.1%}')
            else:
                widget.set_title(f'{text}: {value}')

        return update

    def force_update_labels(self):
        for label in self.labels:
            label.apply_draw_callbacks()

    def get_theme(self):
        theme = super().get_theme()
        theme.widget_padding = 1
        theme.widget_margin = (10, 0)
        theme.widget_alignment = pgmen.locals.ALIGN_LEFT
        return theme
