import pygame_menu as pgmen

from constructs.construct_type import ConstructType
from panels.panel import Panel


class UpgradePanel(Panel):
    IMAGE_SIZE = 100

    def __init__(self, width, height, game_window, simulation):
        super().__init__(width, height, game_window)
        self.menu = pgmen.Menu(title='LOT', width=width,
                               height=height, position=(50, 50), rows=50, columns=1,
                               theme=self.get_theme(), enabled=False)

        self.simulation = simulation
        self.control = False
        self.field = None

    def set_field(self, field):
        self.field = field
        self.menu.clear()

        # IMAGE & INFO
        info = field.construct.get_level()

        self.menu.add.image(
            field.construct.image_path,
            scale=(self.IMAGE_SIZE / field.construct.image.get_width(),
                   self.IMAGE_SIZE / field.construct.image.get_width())
        )

        if field.construct_level + 1 in field.construct.type['level']:
            self.menu.add.label(
                f'upgrade cost: {field.construct.type["level"][field.construct_level + 1]["upgrade_cost"]}')
            self.menu.add.button('UPGRADE', self.upgrade)

        self.menu.add.label('')
        for key, value in info.items():
            if key == 'images':
                continue
            self.menu.add.label(
                f'{key.replace("_", " ")}: {value}', max_char=30)
        self.menu.add.label(f'max level: {len(field.construct.type["level"])}')
        self.menu.add.label(
            'Heat: ' + str(field.construct.heat), max_char=30)
        self.menu.add.label(
            'Crime: ' + str(field.construct.crime_level), max_char=30)
        self.menu.add.label(
            'satisfaction: ' + str(field.construct.satisfaction), max_char=30)

        self.menu.add.label(
            f'COST: {field.construct.type["cost"]}')

        self.menu.force_surface_cache_update()

    def upgrade(self):
        self.control = not self.control
        if self.control and self.simulation.can_buy(construct=ConstructType[self.field.construct.type_name],
                                                    level=self.field.construct_level + 1):
            self.simulation.integrate_construct(self.field, remove=True)
            self.field.construct.level_up()
            self.field.construct_level += 1
            self.simulation.integrate_construct(self.field)
            self.menu.disable()

    def get_theme(self):
        theme = super().get_theme()
        theme.widget_font_size = 25
        return theme
