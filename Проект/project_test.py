import unittest
import pygame
from pygame import sprite, image, transform
import os

class Proekt(sprite.Sprite):
    def __init__(self, x, y, speed, mg):
        sprite.Sprite.__init__(self)
        self.speed = speed
        mg = image.load(mg)
        self.image = transform.scale(mg, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class TestProekt(unittest.TestCase):
    def setUp(self):
        pygame.init()

        # Создаем временное изображение для теста
        self.test_image_path = 'test_image.png'
        surface = pygame.Surface((10, 10))
        surface.fill((0, 255, 0))
        pygame.image.save(surface, self.test_image_path)

    def tearDown(self):
        pygame.quit()
        # Удаляем файл изображения после теста
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)

    def test_proekt_initialization(self):
        x, y, speed = 150, 250, 5
        sprite_obj = Proekt(x, y, speed, self.test_image_path)

        # Проверка положения
        self.assertEqual(sprite_obj.rect.x, x)
        self.assertEqual(sprite_obj.rect.y, y)

        # Проверка скорости
        self.assertEqual(sprite_obj.speed, speed)

        # Проверка размера изображения
        self.assertEqual(sprite_obj.image.get_size(), (50, 50))

        # Проверка, что изображение загружено
        self.assertIsNotNone(sprite_obj.image)

if name == '__main__':
    unittest.main()
