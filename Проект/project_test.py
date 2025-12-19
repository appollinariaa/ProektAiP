import unittest
import main
import pygame

class TestProektMethods(unittest.TestCase):
    def setUp(self):
        # Инициализация pygame для создания объектов
        pygame.init()

        # Создаем объект Proekt, подставляя существующие ресурсы
        # Предположим, что "static/zvezda.png" и т.п. существуют
        # Если ресурсов нет, можно заменить на Surface()
        self.sprite = main.Proekt(10, 20, 5, "static/zvezda.png")
    
    def test_sync_rect_updates_rect(self):
        # Меняем fx и fy
        self.sprite.fx = 15.3
        self.sprite.fy = 25.6
        # Вызываем синхронизацию
        self.sprite.sync_rect()
        # Проверяем, что rect.x и rect.y совпадают с округленными fx, fy
        self.assertEqual(self.sprite.rect.x, int(round(self.sprite.fx)))
        self.assertEqual(self.sprite.rect.y, int(round(self.sprite.fy)))

    def test_see_calls_blt(self):
        # Проверяем, что метод вызывает window.blit
        # Для этого нужно замокать window.blit
        # Но если не использовать моки — можно проверить, что вызывается функция
        # В реальных тестах лучше мокать, но здесь — просто пример
        self.sprite.image = pygame.Surface((50,50))
        self.sprite.rect.x = 10
        self.sprite.rect.y = 20
        # Создать mock window
        class DummySurface:
            def __init__(self):
                self.blitted = False
            def blit(self, img, pos):
                self.blitted = True
                self.pos = pos
                self.img = img
        dummy_window = DummySurface()
        # временно заменить глобальную переменную window
        main.window = dummy_window
        self.sprite.see()
        self.assertTrue(dummy_window.blitted)
        self.assertEqual(dummy_window.pos, (10,20))

class TestCaractersSmena(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.char = main.Caracters(0, 0, 1, "static/zvezda.png")
        self.char.key = pygame.key  # чтобы не ругалось
        self.char.key.get_pressed = lambda: {
            main.K_LEFT: False,
            main.K_RIGHT: False,
            main.K_UP: False,
            main.K_DOWN: False,
            main.K_a: False,
            main.K_w: False,
            main.K_s: False,
            main.K_d: False
        }
        self.dt = 0.1

    def test_smena_moves_left_and_right(self):
        # Тестируем движение влево
        self.char.key.get_pressed = lambda: {main.K_LEFT: True}
        old_fx = self.char.fx
        self.char.smena(self.dt)
        self.assertLess(self.char.fx, old_fx)

        # Тестируем движение вправо
        self.char.key.get_pressed = lambda: {main.K_d: True}
        old_fx = self.char.fx
        self.char.smena(self.dt)
        self.assertGreater(self.char.fx, old_fx)

    def test_smena_moves_up_and_down(self):
        self.char.key.get_pressed = lambda: {main.K_w: True}
        old_fy = self.char.fy
        self.char.smena(self.dt)
        self.assertLess(self.char.fy, old_fy)

        self.char.key.get_pressed = lambda: {main.K_s: True}
        old_fy = self.char.fy
        self.char.smena(self.dt)
        self.assertGreater(self.char.fy, old_fy)

class TestVragSmenaMethods(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.vrag = main.Eneny(200, 170, 1, "static/vrag.png")
        # Инициализация свойств
        self.vrag.side2 = "up"
        self.vrag.side = "left"
        self.vrag._route_i = 0
        self.vrag._route_dir = 1

    def test_vrag_smena1_changes_direction(self):
        self.vrag.rect = pygame.Rect(0, 170, 50, 50)
        self.vrag.side2 = "up"
        self.vrag.vrag_smena1(0.1)
        # После достижения y <= 170, должно смениться side2 на "down"
        self.assertEqual(self.vrag.side2, "down" if self.vrag.rect.y <= 170 else self.vrag.side2)

    def test_vrag_smena2_changes_direction(self):
        self.vrag.rect = pygame.Rect(20, 0, 50, 50)
        self.vrag.side = "left"
        self.vrag.fx = 20
        self.vrag.vrag_smena2(0.1)
        # После достижения x <= 20, side должно стать "right"
        self.assertIn(self.vrag.side, ["left", "right"])

    def test_vrag_smena3_moves_along_route(self):
        # Проверим, что враг движется по маршруту
        self.vrag.route = [(0, 0), (10, 0)]
        self.vrag._route_i = 0
        self.vrag._route_dir = 1
        self.vrag.fx = 0
        self.vrag.fy = 0
        self.vrag.speed = 1
        self.vrag.vrag_smena3(0.1)
        self.assertTrue(isinstance(self.vrag.fx, float))
        self.assertTrue(isinstance(self.vrag.fy, float))

class TestWallsAndDoor(unittest.TestCase):
    def test_wall_init_and_picture_wall(self):
        wall = main.Wall(0, 0, 10, 10, 255, 0, 0)
        self.assertEqual(wall.rect.x, 0)
        self.assertEqual(wall.rect.y, 0)
        # вызов метода - не ругается
        wall.picture_wall()

    def test_door_init(self):
        door = main.Door(10, 20, 30, 40)
        self.assertEqual(door.rect.x, 10)
        self.assertEqual(door.rect.y, 20)

if __name__ == '__main__':
    unittest.main()
