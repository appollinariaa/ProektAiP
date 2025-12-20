import unittest  
import pygame  
from your_module import Proekt, Caracters, Eneny, Wall, Door  # Импортируйте ваш код


class TestProekt(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.proekt = Proekt(10, 10, 5, "path/to/image.png")

    def test_init(self):
        self.assertEqual(self.proekt.fx, 10)
        self.assertEqual(self.proekt.fy, 10)
        self.assertEqual(self.proekt.speed, 5)
        self.assertIsNotNone(self.proekt.image)
        self.assertIsInstance(self.proekt.rect, pygame.Rect)

    def test_sync_rect(self):
        self.proekt.fx = 20.5  
        self.proekt.fy = 30.5  
        self.proekt.sync_rect()
        self.assertEqual(self.proekt.rect.x, 21)
        self.assertEqual(self.proekt.rect.y, 30)

    def test_see(self):
        # Проверка, что метод see не вызывает ошибок.
        try:
            self.proekt.see()
        except Exception as e:
            self.fail(f"see() raised an exception {e}")


class TestCaracters(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.caracter = Caracters(15, 500, 15, "path/to/image.png")

    def test_smena(self):
        dt = 1.0  
        self.caracter.smena(dt)
        self.assertNotEqual(self.caracter.fx, 15.0)  # Проверяем, что позиция изменилась


class TestEneny(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.enemy = Eneny(100, 100, 10, "path/to/image.png")

    def test_vrag_smena1(self):
        dt = 1.0  
        self.enemy.vrag_smena1(dt)
        self.assertTrue(self.enemy.fy < 100)  # Проверяем, что враг переместился вверх

    def test_vrag_smena2(self):
        dt = 1.0  
        self.enemy.vrag_smena2(dt)
        self.assertTrue(self.enemy.fx > 100)  # Проверяем, что враг переместился вправо


class TestWall(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.wall = Wall(0, 0, 100, 20, 255, 0, 0)

    def test_init(self):
        self.assertEqual(self.wall.rect.width, 20)
        self.assertEqual(self.wall.rect.height, 100)


class TestDoor(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.door = Door(800, 100, 50, 20)

    def test_init(self):
        self.assertEqual(self.door.rect.x, 800)
        self.assertEqual(self.door.rect.y, 100)


if __name__ == '__main__':
    unittest.main()
   - Например, в тесте `test_smena` проверяется, что после вызова метода перемещения `smena` координаты игрока изменились.

4. **Запуск тестов**: Тесты запускаются, если файл выполняется как основной.

Убедитесь, что пути к изображениям, которые вы используете в ваших классах, корректны. Тесты могут не пройти, если изображения не найдены.
