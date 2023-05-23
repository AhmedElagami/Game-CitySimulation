import sys
import os

# Get the parent directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to the system path
sys.path.append(parent_dir)

import unittest
import pygame as pg
import pygame_menu as pgmen
from panels.panel import Panel


class PanelTestCase(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.game_window = pg.display.set_mode((800, 600))
        self.panel = Panel(200, 100, self.game_window)

    def test_get_theme(self):
        theme = self.panel.get_theme()
        self.assertIsInstance(theme, pgmen.themes.Theme)

    def test_draw_menu_enabled(self):
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.menu.enable()
        self.panel.draw(self.game_window)
        # Add assertions to check if the menu is drawn correctly

    def test_draw_menu_disabled(self):
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.draw(self.game_window)
        # Add assertions to check if the menu is not drawn

    def test_handle_menu_enabled(self):
        event = pg.event.Event(pg.KEYDOWN, {'key': pg.K_RETURN})
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.menu.enable()
        self.panel.handle(event)
        # Add assertions to check if the event is handled correctly

    def test_handle_menu_disabled(self):
        event = pg.event.Event(pg.KEYDOWN, {'key': pg.K_RETURN})
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.handle(event)
        # Add assertions to check if the event is not handled

    def test_is_enabled(self):
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.menu.enable()
        self.assertTrue(self.panel.is_enabled())

    def test_enable(self):
        self.panel.enable()
        self.assertTrue(self.panel.is_enabled())

    def test_disable(self):
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.disable()
        self.assertFalse(self.panel.is_enabled())

    def test_collide_menu_enabled_inside(self):
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.menu.enable()
        pg.mouse.set_pos((100, 50))
        self.assertTrue(self.panel.collide())

    def test_collide_menu_enabled_outside(self):
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.menu.enable()
        pg.mouse.set_pos((300, 200))
        self.assertFalse(self.panel.collide())

    def test_collide_menu_disabled(self):
        self.panel.menu = pgmen.Menu(200, 100)
        pg.mouse.set_pos((100, 50))
        self.assertFalse(self.panel.collide())

    def test_get_subpanels(self):
        subpanels = self.panel.get_subpanels()
        self.assertIsInstance(subpanels, list)

    def test_disable_subpanels(self):
        subpanel = Panel(100, 50, self.game_window)
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.menu.enable()
        self.panel.menu.add.generic_widget(subpanel.menu)
        self.panel.disable_subpanels()
        self.assertFalse(subpanel.menu.is_enabled())

    def test_disable_all_panels(self):
        subpanel = Panel(100, 50, self.game_window)
        subpanel.menu = pgmen.Menu(100, 50)
        subpanel.menu.enable()
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.menu.enable()
        self.panel.menu.add.generic_widget(subpanel.menu)
        self.panel.disable_all_panels()
        self.assertFalse(self.panel.menu.is_enabled())
        self.assertFalse(subpanel.menu.is_enabled())

    def test_unselect_selected_widget(self):
        widget = pgmen.widgets.Button('Button')
        self.panel.menu = pgmen.Menu(200, 100)
        self.panel.menu.enable()
        self.panel.menu.add.generic_widget(widget)
        widget.select()
        self.panel.unselect_selected_widget()
        self.assertFalse(widget.is_selected())

    def tearDown(self):
        pg.quit()


if __name__ == '__main__':
    unittest.main()
