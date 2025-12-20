import unittest
import pygame
from pygame import *
import sys

# Импортируем классы из вашего файла, предположим, он называется main.py
import main

class TestProekt(unittest.TestCase):
    def setUp(self):
        pygame.init()
        # Создаем временный Surface для изображений
        self.test_surface = pygame.Surface((10, 10))
        # Патчим image.load, чтобы возвращал тестовый Surface
        main.image.load = lambda path: self.test_surface

    def tearDown(self):
        pygame.quit()

    def test_init_sets_correctly(self):
        sprite_obj = main.Proekt(10.5, 20.5, 5, "dummy.png")
        self.assertEqual(sprite_obj.rect.width, 50)
        self.assertEqual(sprite_obj.rect.height, 50)
        self.assertEqual(sprite_obj.rect.x, int(round(sprite_obj.fx)))
        self.assertEqual(sprite_obj.rect.y, int(round(sprite_obj.fy)))
        self.assertEqual(sprite_obj.fx, 10.5)
        self.assertEqual(sprite_obj.fy, 20.5)

    def test_sync_rect_updates_rect(self):
        sprite_obj = main.Proekt(0, 0, 1, "dummy.png")
        sprite_obj.fx = 15.7
        sprite_obj.fy = 25.3
        sprite_obj.sync_rect()
        self.assertEqual(sprite_obj.rect.x, int(round(sprite_obj.fx)))
        self.assertEqual(sprite_obj.rect.y, int(round(sprite_obj.fy)))

    def test_see_calls_blit(self):
        sprite_obj = main.Proekt(0, 0, 1, "dummy.png")
        # Мокаем window.blit
        class DummyWin:
            def __init__(self):
                self.calls = []
            def blit(self, img, pos):
                self.calls.append((img, pos))
        dummy_window = DummyWin()
        main.window = dummy_window
        sprite_obj.see()
        self.assertEqual(len(dummy_window.calls), 1)
        self.assertEqual(dummy_window.calls[0][1], (sprite_obj.rect.x, sprite_obj.rect.y))

class TestCaracters(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.char = main.Caracters(0, 0, 1, "dummy.png")
        # Мокаем get_pressed
        self.pressed_keys = {}
        main.key.get_pressed = lambda: self.pressed_keys

    def tearDown(self):
        pygame.quit()

    def test_smena_moves_left_right_up_down(self):
        self.pressed_keys = {main.K_LEFT: True}
        old_fx = self.char.fx
        self.char.smena(0.1)
        self.assertLess(self.char.fx, old_fx)

        self.pressed_keys = {main.K_RIGHT: True}
        old_fx = self.char.fx
        self.char.smena(0.1)
        self.assertGreater(self.char.fx, old_fx)

        self.pressed_keys = {main.K_w: True}
        old_fy = self.char.fy
        self.char.smena(0.1)
        self.assertLess(self.char.fy, old_fy)

        self.pressed_keys = {main.K_s: True}
        old_fy = self.char.fy
        self.char.smena(0.1)
        self.assertGreater(self.char.fy, old_fy)

class TestVragSmena(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.vrag = main.Eneny(100, 170, 1, "dummy.png")
        # Инициализация свойств
        self.vrag.side2 = "up"
        self.vrag.side = "left"
        self.vrag._route_i = 0
        self.vrag._route_dir = 1
        # Мокаем get_pressed
        main.key.get_pressed = lambda: {}
        # Мокаем sync_rect
        self.vrag.sync_rect = lambda: None

    def tearDown(self):
        pygame.quit()

    def test_vrag_smena1_changes_direction(self):
        self.vrag.rect.y = 170
        self.vrag.vrag_smena1(0.1)
        self.assertIn(self.vrag.side2, ["up", "down"])

    def test_vrag_smena2_changes_direction(self):
        self.vrag.rect.x = 20
        self.vrag.side = "left"
        self.vrag.fx = 20
        self.vrag.vrag_smena2(0.1)
        self.assertIn(self.vrag.side, ["left", "right"])

        self.vrag.rect.x = 730
        self.vrag.side = "right"
        self.vrag.fx = 730
        self.vrag.vrag_smena2(0.1)
        self.assertIn(self.vrag.side, ["left", "right"])

    def test_vrag_smena3_moves_along_route(self):
        self.vrag.route = [(0,0), (10,0)]
        self.vrag._route_i = 0
        self.vrag._route_dir = 1
        self.vrag.fx = 0
        self.vrag.fy = 0
        self.vrag.speed = 1
        self.vrag.vrag_smena3(0.1)
        self.assertIsInstance(self.vrag.fx, float)
        self.assertIsInstance(self.vrag.fy, float)

        # Проверка разворота при достижении конца маршрута
        self.vrag._route_i = len(self.vrag.route) - 1
        self.vrag.fx, self.vrag.fy = 0, 0
        self.vrag._route_dir = 1
        self.vrag.vrag_smena3(0.1)
        self.assertEqual(self.vrag._route_dir, -1)

class TestWallAndDoor(unittest.TestCase):
    def setUp(self):
        pygame.init()
        # Создаем окно для draw.rect
        main.window = pygame.Surface((810, 800))
        # Создаем стену
        self.wall = main.Wall(10, 20, 30, 40, 255, 0, 0)

    def tearDown(self):
        pygame.quit()

    def test_wall_init(self):
        self.assertEqual(self.wall.rect.x, 10)
        self.assertEqual(self.wall.rect.y, 20)
        self.assertEqual(self.wall.rect.width, 40)
        self.assertEqual(self.wall.rect.height, 30)

    def test_picture_wall_calls_draw(self):
        # Проверяем, что draw.rect вызывается с правильными аргументами
        called_args = {}
        def fake_draw_rect(surface, color, rect):
            called_args['surface'] = surface
            called_args['color'] = color
            called_args['rect'] = rect
        main.draw.rect = fake_draw_rect
        self.wall.picture_wall()
        self.assertEqual(called_args['color'], (self.wall.r, self.wall.g, self.wall.b))
        self.assertEqual(called_args['rect'], (self.wall.rect.x, self.wall.rect.y, self.wall.width, self.wall.height))

class TestDoor(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.door = main.Door(50, 60, 70, 80)

    def tearDown(self):
        pygame.quit()

    def test_init(self):
        self.assertEqual(self.door.rect.x, 50)
        self.assertEqual(self.door.rect.y, 60)
        self.assertEqual(self.door.rect.width, 80)
        self.assertEqual(self.door.rect.height, 70)

if __name__ == '__main__':
    unittest.main()
