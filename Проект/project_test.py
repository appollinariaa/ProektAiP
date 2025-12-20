import unittest
from unittest.mock import patch, MagicMock
from main import Proekt
import pygame
import os

class TestProekt(unittest.TestCase):

    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_init(self):
        proekt = Proekt(0, 0, 5, 'image.png')
        self.assertEqual(proekt.rect.x, 0)
        self.assertEqual(proekt.rect.y, 0)
        self.assertEqual(proekt.speed, 5)

    def test_image_loaded(self):
        try:
            Proekt(0, 0, 5, 'image.png')
        except pygame.error:
            self.fail("Изображение не загрузилось")

    def test_invalid_image(self):
        with self.assertRaises(pygame.error):
            Proekt(0, 0, 5, 'nonexistent_image.png')

class TestSpriteMethods(unittest.TestCase):

    def setUp(self):
        self.obj = YourClassName()  # Создание объекта для тестирования

    @patch('pygame.display.get_surface')
    def test_see(self, mock_window):
        mock_window.return_value = MagicMock()
        self.obj.rect.x = 10
        self.obj.rect.y = 20
        self.obj.image = MagicMock()
        self.obj.see()
        mock_window.return_value.blit.assert_called_once_with(self.obj.image, (10, 20))

    def test_sync_rect(self):
        self.obj.fx = 15.7
        self.obj.fy = 25.3
        self.obj.rect.x = 0
        self.obj.rect.y = 0
        self.obj.sync_rect()
        self.assertEqual(self.obj.rect.x, 16)
        self.assertEqual(self.obj.rect.y, 25)

class TestCaracters(unittest.TestCase):

    def setUp(self):
        self.caracter = Caracters()
        self.caracter.speed = 100
        self.caracter.fx = 0
        self.caracter.fy = 0

    @patch('pygame.key.get_pressed')
    def test_smena_left(self, mock_keys):
        mock_keys.return_value = {pygame.K_LEFT: 1, pygame.K_a: 0}
        with patch('pygame.time.get_ticks'):
            self.caracter.smena(0.01)
        self.assertEqual(self.caracter.fx, -1)

    @patch('pygame.key.get_pressed')
    def test_smena_right(self, mock_keys):
        mock_keys.return_value = {pygame.K_RIGHT: 1, pygame.K_d: 0}
        with patch('pygame.time.get_ticks'):
            self.caracter.smena(0.01)
        self.assertEqual(self.caracter.fx, 1)

    @patch('pygame.key.get_pressed')
    def test_smena_up(self, mock_keys):
        mock_keys.return_value = {pygame.K_UP: 1, pygame.K_w: 0}
        with patch('pygame.time.get_ticks'):
            self.caracter.smena(0.01)
        self.assertEqual(self.caracter.fy, -1)

    @patch('pygame.key.get_pressed')
    def test_smena_down(self, mock_keys):
        mock_keys.return_value = {pygame.K_DOWN: 1, pygame.K_s: 0}
        with patch('pygame.time.get_ticks'):
            self.caracter.smena(0.01)
        self.assertEqual(self.caracter.fy, 1)

    @patch.object(Caracters, 'sync_rect')
    @patch('pygame.key.get_pressed')
    def test_sync_rect_called(self, mock_keys, mock_sync_rect):
        mock_keys.return_value = {}
        self.caracter.smena(0.01)
        mock_sync_rect.assert_called_once()

class TestEneny(unittest.TestCase):

    def setUp(self):
        self.enemy = Eneny()
        self.enemy.rect.y = 200  # Начальная позиция
        self.enemy.speed = 100
        self.enemy.SPEED_FACTOR = 1.0

    def test_move_down(self):
        with patch.object(Eneny, 'sync_rect'):
            self.enemy.vrag_smena1(0.01)
            self.assertEqual(self.enemy.fy, 1)

    def test_move_up(self):
        self.enemy.rect.y = 430
        with patch.object(Eneny, 'sync_rect'):
            self.enemy.vrag_smena1(0.01)
            self.assertEqual(self.enemy.fy, -1)

    def test_change_direction(self):
        self.enemy.rect.y = 170
        self.enemy.vrag_smena1(0.01)
        self.assertEqual(self.enemy.side2, "down")

class TestYourClassName(unittest.TestCase):

    def test_init(self):
        obj = YourClassName(10, 20, 30, 40, 255, 0, 0)
        self.assertEqual(obj.r, 255)
        self.assertEqual(obj.g, 0)
        self.assertEqual(obj.b, 0)
        self.assertEqual(obj.width, 30)
        self.assertEqual(obj.height, 40)
        self.assertIsInstance(obj.image, pygame.Surface)
        self.assertIsInstance(obj.rect, pygame.Rect)

    @patch('pygame.draw.rect')
    def test_picture_wall(self, mock_draw_rect):
        obj = YourClassName(10, 20, 30, 40, 255, 0, 0)
        obj.picture_wall()
        mock_draw_rect.assert_called_once_with(window, (255, 0, 0), (10, 20, 30, 40))
        
if name == '__main__':
    unittest.main()
