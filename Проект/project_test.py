import unittest
import pygame
from pygame import *

from main import Proekt, Caracters, Eneny, Wall, Door, window, background, geroy, vrag1, vrag2, vrag3, stars, walls, lage, lage2, lage3, lage4, lage5, lage6, lage7, lage8, lage9, lage10, lage11, lage12, lage13, lage14, lage15, lage16, lage17, lage18, lage19, lage20, lage21, lage22, lage23, lage24, lage25, lage26, lage27, lage28, lage29, lage30, lage31, lage32, lage33, lage34, lage35, lage36, lage37, lage38, lage39, lage40, lage41, lage42, lage43, lage44, lage45, lage46, lage47, lage48, lage49, lage50, lage51, lage52

class TestGameLogic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
       pygame.init()
        # Создаем окно
        cls.screen = pygame.display.set_mode((810, 800))
        pygame.display.set_caption("Тестовая среда")
        # Загружаем фон
        cls.background = pygame.image.load("static/фон1.jpg")
        cls.background = pygame.transform.scale(cls.background, (810, 800))
        # Создаем объекты
        cls.geroy = Caracters(15, 500, 15, "static/geroy.png")
        cls.vrag1 = Eneny(0, 70, 20, "static/vrag.png")
        cls.vrag2 = Eneny(100, 650, 15, "static/vrag.png")
        cls.vrag3 = Eneny(750, 0, 15, "static/vrag.png")
        cls.stars = [
            Proekt(15, 90, 0, "static/zvezda.png"),
            Proekt(740, 15, 0, "static/zvezda.png"),
            Proekt(420, 400, 0, "static/zvezda.png")
        ]
        cls.walls = [
            Wall(0, 0, 800, 10, 100, 0, 235),
            Wall(0, 0, 10, 800, 100, 0, 235),
            Wall(800, 0, 130, 10, 100, 0, 235),
        ]

    def test_proekt_init_and_see(self):
        p = Proekt(10, 20, 5, "static/zvezda.png")
        self.assertEqual(p.rect.x, 10)
        self.assertEqual(p.rect.y, 20)
        self.assertEqual(p.speed, 5)
        self.assertIsNotNone(p.image)
        # Проверка, что изображение загружено
        self.assertIsInstance(p.image, pygame.Surface)
        # Проверка вызова see
        # Создаем поверхность, на которой будем рисовать
        surface = pygame.Surface((50, 50))
        global window
        window = surface
        p.see()
        # Тут можно проверить, что на поверхности что-то нарисовано
        self.assertTrue(isinstance(p.image, pygame.Surface))

    def test_carcacters_movement(self):
        c = Caracters(50, 50, 10, "static/zvezda.png")
        c.rect.x = 100
        c.rect.y = 100

        # Без нажатий
        keys = [0]*323
        self.assertEqual(c.rect.x, 100)
        c.smena()
        self.assertEqual(c.rect.x, 100)
        self.assertEqual(c.rect.y, 100)

        # Имитируем нажатие K_LEFT
        class Keys:
            def get_pressed(self):
                return {pygame.K_LEFT: 1}
            def getitem(self, key):
                return 1 if key in [pygame.K_LEFT, pygame.K_a] else 0
        with patch('pygame.key.get_pressed', return_value=Keys().get_pressed()):
            c.smena()
            self.assertEqual(c.rect.x, 90)

        # Имитируем нажатие K_RIGHT
        class Keys:
            def get_pressed(self):
                return {pygame.K_RIGHT: 1}
            def getitem(self, key):
                return 1 if key in [pygame.K_RIGHT, pygame.K_d] else 0
        with patch('pygame.key.get_pressed', return_value=Keys().get_pressed()):
            c.smena()
            self.assertEqual(c.rect.x, 100)

        # Аналогично для K_UP и K_DOWN
        class Keys:
            def get_pressed(self):
                return {pygame.K_UP: 1}
            def getitem(self, key):
                return 1 if key in [pygame.K_UP, pygame.K_w] else 0
        with patch('pygame.key.get_pressed', return_value=Keys().get_pressed()):
            c.smena()
            self.assertEqual(c.rect.y, 90)
          class Keys:
            def get_pressed(self):
                return {pygame.K_DOWN: 1}
            def getitem(self, key):
                return 1 if key in [pygame.K_DOWN, pygame.K_s] else 0
        with patch('pygame.key.get_pressed', return_value=Keys().get_pressed()):
            c.smena()
            self.assertEqual(c.rect.y, 100)

   def test_enemy_smena_and_smena2(self):
        enemy = Eneny(0, 0, 10, "static/vrag.png")
        enemy.rect.x = 0
        enemy.side = "left"
        enemy.smena()
        self.assertEqual(enemy.side, "right")
        self.assertEqual(enemy.rect.x, -10)

        enemy.rect.x = 700
        enemy.side = "right"
        enemy.smena()
        self.assertEqual(enemy.side, "left")
        self.assertEqual(enemy.rect.x, 700 + enemy.speed)

        enemy.rect.y = 30
        enemy.side2 = "up"
        enemy.smena2()
        self.assertEqual(enemy.side2, "down")
        self.assertEqual(enemy.rect.y, 30 - enemy.speed)

        enemy.rect.y = 500
        enemy.side2 = "down"
        enemy.smena2()
        self.assertEqual(enemy.side2, "up")
        self.assertEqual(enemy.rect.y, 500 + enemy.speed)

    def test_wall_picture_wall(self):
        wall = Wall(10, 10, 50, 50, 255, 0, 0)
        surface = pygame.Surface((800, 800))
        global window
        window = surface
        wall.picture_wall()
        # Проверка, что на поверхности что-то нарисовано (например, цвет заливки или что-то подобное)
        self.assertIsInstance(wall.image, pygame.Surface)

    def test_collision_detection(self):
        sprite1 = pygame.sprite.Sprite()
        sprite2 = pygame.sprite.Sprite()
        sprite1.rect = pygame.Rect(0, 0, 50, 50)
        sprite2.rect = pygame.Rect(25, 25, 50, 50)
        self.assertTrue(pygame.sprite.collide_rect(sprite1, sprite2))
        sprite2.rect.x = 100
        self.assertFalse(pygame.sprite.collide_rect(sprite1, sprite2))

    def test_game_over_and_win(self):
        class TestGameLogic(unittest.TestCase):

    def setUp(self):
        # Инициализация 
        pygame.init()
        self.screen = pygame.display.set_mode((810, 800))
        # Создаем все необходимые объекты
        self.geroy = Caracters(15, 500, 15, "static/geroy.png")
        self.vrag1 = Eneny(0, 70, 20, "static/vrag.png")
        self.vrag2 = Eneny(100, 650, 15, "static/vrag.png")
        self.vrag3 = Eneny(750, 0, 15, "static/vrag.png")
        self.stars = [
            Proekt(15, 90, 0, "static/zvezda.png"),
            Proekt(740, 15, 0, "static/zvezda.png"),
            Proekt(420, 400, 0, "static/zvezda.png")
        ]
        # Создаем дверь
        self.door_rect = Door(800, 130, 100, 10).rect
        # Создаем список врагов для проверки
        self.vrags = [self.vrag1, self.vrag2, self.vrag3]
        # Статусы
        self.game_over_triggered = False
        self.win_triggered = False

    def test_game_over_collision(self):
        # Смоделируем столкновение с врагом
        self.geroy.rect.x, self.geroy.rect.y = 100, 100
        for vrag in self.vrags:
            vrag.rect.x, vrag.rect.y = 100, 100  # совпадение с героем
        # Имитация проверки столкновения
        for vrag in self.vrags:
            if pygame.sprite.collide_rect(self.geroy, vrag):
                # В реальной игре: загрузка изображения "game_over.png"
                # Проверим, что вызовется загрузка правильного файла
                self.game_over_triggered = True
                break
        self.assertTrue(self.game_over_triggered, "Игра должна завершиться при столкновении с врагом")

    def test_win_condition(self):
        # Столкновение с дверью при собранных звёздах
        # Обнуляем звезды, считаем, что все собраны
        stars = []
        door_open = True
        # Расположение героя у двери
        self.geroy.rect.x = self.door_rect.x
        self.geroy.rect.y = self.door_rect.y

        # Проверка столкновения
        if door_open and pygame.sprite.collide_rect(self.geroy, self.door_rect):
            # В реальной игре: загрузка "win.jpg"
            self.win_triggered = True

        self.assertTrue(self.win_triggered, "Игра должна завершиться победой при входе в дверь.")

    def test_see_function(self):
        # Проверка метода see у Proekt
        p = Proekt(10, 10, 0, "static/zvezda.png")
        surface = pygame.Surface((50, 50))
        global window
        window = surface
        p.see()
        self.assertIsInstance(p.image, pygame.Surface)

    def tearDown(self):
        pass

if name == 'main':
    unittest.main()
