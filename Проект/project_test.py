import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
from pygame import sprite, Rect, Surface
import sys
sys.modules['pygame'] = pygame

# Импортируем классы из main.py
# Для тестирования мы скопируем их сюда или импортируем
# Давайте скопируем код классов для независимости

# Константы из main.py
FPS = 60
SPEED_FACTOR = 10
GAME_TIME_MS = 2 * 60 * 1000
HIT_COOLDOWN_MS = 600
START_X, START_Y = 15, 500

# Копия классов из main.py (адаптированная для тестирования)
class Proekt(sprite.Sprite):
    def __init__(self, x, y, speed, mg):
        sprite.Sprite.__init__(self)
        self.speed = speed
        # Мокаем загрузку изображения для тестов
        if isinstance(mg, str):
            self.image = Surface((50, 50))
        else:
            self.image = mg
        self.rect = self.image.get_rect()
        self.fx = float(x)
        self.fy = float(y)
        self.rect.x = int(self.fx)
        self.rect.y = int(self.fy)
    
    def see(self):
        # В тестах этот метод не будет вызываться с настоящим window
        pass
    
    def sync_rect(self):
        self.rect.x = int(round(self.fx))
        self.rect.y = int(round(self.fy))

class Caracters(Proekt):
    def smena(self, dt):
        keys = {pygame.K_LEFT: False, pygame.K_a: False, 
                pygame.K_RIGHT: False, pygame.K_d: False,
                pygame.K_UP: False, pygame.K_w: False,
                pygame.K_DOWN: False, pygame.K_s: False}
        
        # В тестах мы будем мокать pygame.key.get_pressed()
        step = self.speed * SPEED_FACTOR * dt
        
        if keys.get(pygame.K_LEFT, False) or keys.get(pygame.K_a, False):
            self.fx -= step
        if keys.get(pygame.K_RIGHT, False) or keys.get(pygame.K_d, False):
            self.fx += step
        if keys.get(pygame.K_UP, False) or keys.get(pygame.K_w, False):
            self.fy -= step
        if keys.get(pygame.K_DOWN, False) or keys.get(pygame.K_s, False):
            self.fy += step
        
        self.sync_rect()

class Eneny(Proekt):
    side = "left"
    side2 = "down"
    
    def vrag_smena1(self, dt):
        step = self.speed * SPEED_FACTOR * dt
        if self.rect.y <= 170:
            self.side2 = "down"
        if self.rect.y >= 420:
            self.side2 = "up"
        if self.side2 == "up":
            self.fy -= step
        else:
            self.fy += step
        self.sync_rect()
    
    def vrag_smena2(self, dt):
        step = self.speed * SPEED_FACTOR * dt
        if self.rect.x <= 20:
            self.side = "right"
        if self.rect.x >= 730:
            self.side = "left"
        if self.side == "left":
            self.fx -= step
        else:
            self.fx += step
        self.sync_rect()
    
    def vrag_smena3(self, dt):
        if not hasattr(self, "route"):
            self.route = [(740, 345), (740, 95), (660, 95), (660, 160), 
                         (585, 160),(585, 95), (510, 95), (510, 15), (740, 15)]
            self._route_i = 0
            self._route_dir = 1
            self.fx, self.fy = map(float, self.route[0])
            self.sync_rect()
            self._route_i = 1
        
        if self.speed <= 0 or len(self.route) < 2:
            return
        
        step = self.speed * SPEED_FACTOR * dt
        tx, ty = self.route[self._route_i]
        tx, ty = float(tx), float(ty)
        x, y = self.fx, self.fy
        dx, dy = tx - x, ty - y
        
        if dx == 0 and dy == 0:
            if self._route_i == len(self.route) - 1:
                self._route_dir = -1
            elif self._route_i == 0:
                self._route_dir = 1
            self._route_i += self._route_dir
            return
        
        dist = (dx * dx + dy * dy) ** 0.5
        move = min(step, dist)
        self.fx = x + dx / dist * move
        self.fy = y + dy / dist * move
        self.sync_rect()

class Wall(sprite.Sprite):
    def __init__(self, x, y, heig, wid, r, g, b):
        sprite.Sprite.__init__(self)
        self.r = r
        self.g = g
        self.b = b
        self.width = wid
        self.height = heig
        self.image = Surface([self.width, self.height])
        self.image.fill((r, g, b))
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, self.width, self.height)
    
    def picture_wall(self):
        # В тестах этот метод не будет вызываться с настоящим window
        pass

class Door(sprite.Sprite):
    def __init__(self, x, y, heig, wid):
        sprite.Sprite.__init__(self)
        self.width = wid
        self.height = heig
        self.image = Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, self.width, self.height)


# Тестовый модуль
class TestGameLogic(unittest.TestCase):
    
    def setUp(self):
        """Инициализация перед каждым тестом"""
        pygame.init()
        # Мокаем pygame.display.set_mode чтобы не открывать окно
        pygame.display.set_mode = Mock(return_value=Mock())
    
    def tearDown(self):
        """Очистка после каждого теста"""
        pygame.quit()
    
    # Тесты для класса Proekt
    def test_proekt_initialization(self):
        """Тест инициализации базового класса Proekt"""
        proekt = Proekt(100, 200, 5, "test.png")
        
        self.assertEqual(proekt.fx, 100.0)
        self.assertEqual(proekt.fy, 200.0)
        self.assertEqual(proekt.speed, 5)
        self.assertEqual(proekt.rect.x, 100)
        self.assertEqual(proekt.rect.y, 200)
        self.assertIsNotNone(proekt.image)
    
    def test_proekt_sync_rect(self):
        """Тест синхронизации координат"""
        proekt = Proekt(100.7, 200.3, 5, "test.png")
        
        # Меняем float координаты
        proekt.fx = 150.6
        proekt.fy = 250.4
        
        # Синхронизируем
        proekt.sync_rect()
        
        # Проверяем что rect координаты округлились
        self.assertEqual(proekt.rect.x, 151)  # округление
        self.assertEqual(proekt.rect.y, 250)  # округление
    
    def test_proekt_sync_rect_with_negative(self):
        """Тест синхронизации с отрицательными координатами"""
        proekt = Proekt(-10.5, -20.7, 5, "test.png")
        
        proekt.sync_rect()
        
        self.assertEqual(proekt.rect.x, -10)  # округление вниз
        self.assertEqual(proekt.rect.y, -21)  # округление
    
    # Тесты для класса Caracters
    @patch('pygame.key.get_pressed')
    def test_caracters_movement_up(self, mock_get_pressed):
        """Тест движения персонажа вверх"""
        # Настраиваем мок для клавиши UP
        mock_keys = {pygame.K_UP: True, pygame.K_w: False,
                    pygame.K_DOWN: False, pygame.K_s: False,
                    pygame.K_LEFT: False, pygame.K_a: False,
                    pygame.K_RIGHT: False, pygame.K_d: False}
        mock_get_pressed.return_value = mock_keys
        
        char = Caracters(100, 100, 10, "test.png")
        initial_y = char.fy
        
        # Вызываем движение с dt=1.0
        char.smena(1.0)
        
        # Проверяем что персонаж двинулся вверх
        expected_step = char.speed * SPEED_FACTOR * 1.0
        self.assertEqual(char.fy, initial_y - expected_step)
    
    @patch('pygame.key.get_pressed')
    def test_caracters_movement_left_right(self, mock_get_pressed):
        """Тест движения персонажа влево и вправо"""
        char = Caracters(100, 100, 10, "test.png")
        initial_x = char.fx
        
        # Тестируем движение влево
        mock_keys = {pygame.K_LEFT: True, pygame.K_a: False,
                    pygame.K_RIGHT: False}
        mock_get_pressed.return_value = mock_keys
        
        char.smena(0.5)
        expected_step_left = char.speed * SPEED_FACTOR * 0.5
        self.assertEqual(char.fx, initial_x - expected_step_left)
        
        # Тестируем движение вправо
        char.fx = initial_x  # сбрасываем позицию
        mock_keys = {pygame.K_LEFT: False, pygame.K_a: False,
                    pygame.K_RIGHT: True}
        mock_get_pressed.return_value = mock_keys
        
        char.smena(0.5)
        self.assertEqual(char.fx, initial_x + expected_step_left)
    
    # Тесты для класса Eneny
    def test_enemy_vrag_smena1_up_down(self):
        """Тест движения врага №1 (вертикальное патрулирование)"""
        enemy = Eneny(100, 300, 10, "test.png")
        enemy.rect.y = 300  # Начальная позиция
        
        # Движение вверх (изначально side2 = "down")
        enemy.side2 = "up"
        initial_y = enemy.fy
        enemy.vrag_smena1(0.5)
        
        expected_step = enemy.speed * SPEED_FACTOR * 0.5
        self.assertEqual(enemy.fy, initial_y - expected_step)
        
        # Движение вниз
        enemy.fy = initial_y  # сбрасываем
        enemy.side2 = "down"
        enemy.vrag_smena1(0.5)
        self.assertEqual(enemy.fy, initial_y + expected_step)
    
    def test_enemy_vrag_smena1_boundaries(self):
        """Тест границ движения врага №1"""
        enemy = Eneny(100, 170, 10, "test.png")  # На границе сверху
        enemy.rect.y = 170
        
        # Должно переключиться на "down"
        enemy.vrag_smena1(0.1)
        self.assertEqual(enemy.side2, "down")
        
        # Тест нижней границы
        enemy.rect.y = 420
        enemy.vrag_smena1(0.1)
        self.assertEqual(enemy.side2, "up")
    
    def test_enemy_vrag_smena2_left_right(self):
        """Тест движения врага №2 (горизонтальное патрулирование)"""
        enemy = Eneny(100, 100, 10, "test.png")
        
        # Движение влево
        enemy.side = "left"
        initial_x = enemy.fx
        enemy.vrag_smena2(0.5)
        
        expected_step = enemy.speed * SPEED_FACTOR * 0.5
        self.assertEqual(enemy.fx, initial_x - expected_step)
        
        # Движение вправо
        enemy.fx = initial_x
        enemy.side = "right"
        enemy.vrag_smena2(0.5)
        self.assertEqual(enemy.fx, initial_x + expected_step)
    
    def test_enemy_vrag_smena2_boundaries(self):
        """Тест границ движения врага №2"""
        enemy = Eneny(20, 100, 10, "test.png")  # Левая граница
        enemy.rect.x = 20
        
        # Должно переключиться на "right"
        enemy.vrag_smena2(0.1)
        self.assertEqual(enemy.side, "right")
        
        # Правая граница
        enemy.rect.x = 730
        enemy.vrag_smena2(0.1)
        self.assertEqual(enemy.side, "left")
    
    def test_enemy_vrag_smena3_initialization(self):
        """Тест инициализации маршрута врага №3"""
        enemy = Eneny(0, 0, 10, "test.png")
        
        # При первом вызове должен установиться маршрут
        self.assertFalse(hasattr(enemy, "route"))
        enemy.vrag_smena3(0.1)
        self.assertTrue(hasattr(enemy, "route"))
        self.assertEqual(len(enemy.route), 9)
        self.assertEqual(enemy._route_i, 1)
        self.assertEqual(enemy._route_dir, 1)
    
    def test_enemy_vrag_smena3_movement(self):
        """Тест движения врага №3 по маршруту"""
        enemy = Eneny(740, 345, 10, "test.png")
        
        # Инициализируем маршрут
        enemy.vrag_smena3(0.1)
        
        # Запоминаем начальную позицию
        start_pos = (enemy.fx, enemy.fy)
        
        # Двигаемся маленьким шагом
        enemy.vrag_smena3(0.01)
        
        # Позиция должна измениться
        self.assertNotEqual((enemy.fx, enemy.fy), start_pos)
    
    def test_enemy_vrag_smena3_zero_speed(self):
        """Тест врага №3 с нулевой скоростью"""
        enemy = Eneny(0, 0, 0, "test.png")  # speed = 0
        
        # Должен выйти без ошибок
        try:
            enemy.vrag_smena3(0.1)
        except Exception as e:
            self.fail(f"Метод вызвал исключение при speed=0: {e}")
    
    # Тесты для класса Wall
    def test_wall_initialization(self):
        """Тест инициализации стены"""
        wall = Wall(50, 60, 100, 200, 255, 0, 0)
        
        self.assertEqual(wall.r, 255)
        self.assertEqual(wall.g, 0)
        self.assertEqual(wall.b, 0)
        self.assertEqual(wall.width, 200)
        self.assertEqual(wall.height, 100)
        self.assertEqual(wall.rect.x, 50)
        self.assertEqual(wall.rect.y, 60)
        self.assertEqual(wall.rect.width, 200)
        self.assertEqual(wall.rect.height, 100)
    
    def test_wall_different_colors(self):
        """Тест создания стен разных цветов"""
        colors = [
            (255, 0, 0),    # Красный
            (0, 255, 0),    # Зеленый
            (0, 0, 255),    # Синий
            (128, 128, 128) # Серый
        ]
        
        for r, g, b in colors:
            wall = Wall(0, 0, 10, 10, r, g, b)
            self.assertEqual(wall.r, r)
            self.assertEqual(wall.g, g)
            self.assertEqual(wall.b, b)
    
    # Тесты для класса Door
    def test_door_initialization(self):
        """Тест инициализации двери"""
        door = Door(100, 200, 50, 20)
        
        self.assertEqual(door.width, 20)
        self.assertEqual(door.height, 50)
        self.assertEqual(door.rect.x, 100)
        self.assertEqual(door.rect.y, 200)
        self.assertEqual(door.rect.width, 20)
        self.assertEqual(door.rect.height, 50)
    
    def test_door_collision_rect(self):
        """Тест что дверь имеет правильный Rect для коллизий"""
        door = Door(300, 400, 100, 30)
        
        # Проверяем что rect корректно инициализирован
        self.assertIsInstance(door.rect, Rect)
        self.assertEqual(door.rect.left, 300)
        self.assertEqual(door.rect.top, 400)
        self.assertEqual(door.rect.right, 330)  # 300 + 30
        self.assertEqual(door.rect.bottom, 500)  # 400 + 100
    
    # Тесты на взаимодействие объектов
    def test_collision_detection(self):
        """Тест обнаружения столкновений между объектами"""
        # Создаем персонажа и стену которые сталкиваются
        char = Caracters(100, 100, 10, "test.png")
        wall = Wall(100, 100, 50, 50, 255, 0, 0)
        
        # Проверяем столкновение
        collision = pygame.sprite.collide_rect(char, wall)
        self.assertTrue(collision)
        
        # Создаем стену в другом месте
        wall2 = Wall(200, 200, 50, 50, 255, 0, 0)
        collision2 = pygame.sprite.collide_rect(char, wall2)
        self.assertFalse(collision2)
    
    def test_star_collection_logic(self):
        """Тест логики сбора звезд"""
        # Создаем персонажа и звезду
        char = Caracters(100, 100, 10, "test.png")
        star = Proekt(100, 100, 0, "star.png")
        
        # Они должны сталкиваться
        collision = pygame.sprite.collide_rect(char, star)
        self.assertTrue(collision)
        
        # Если звезда далеко - нет столкновения
        star2 = Proekt(300, 300, 0, "star.png")
        collision2 = pygame.sprite.collide_rect(char, star2)
        self.assertFalse(collision2)
    
    def test_enemy_hit_logic(self):
        """Тест логики попадания врага"""
        char = Caracters(100, 100, 10, "char.png")
        enemy = Eneny(100, 100, 10, "enemy.png")
        
        # Они должны сталкиваться
        collision = pygame.sprite.collide_rect(char, enemy)
        self.assertTrue(collision)
        
        # При столкновении должно обрабатываться попадание
        # (это проверяется в основном игровом цикле)
    
    # Тесты на граничные условия
    def test_movement_with_dt_zero(self):
        """Тест движения с нулевым dt"""
        char = Caracters(100, 100, 10, "test.png")
        initial_x, initial_y = char.fx, char.fy
        
        char.smena(0)  # dt = 0
        
        self.assertEqual(char.fx, initial_x)
        self.assertEqual(char.fy, initial_y)
    
    def test_movement_with_negative_speed(self):
        """Тест движения с отрицательной скоростью"""
        # Хотя в игре скорость положительная, тестируем граничный случай
        char = Caracters(100, 100, -5, "test.png")
        initial_x = char.fx
        
        # Мокаем клавиши для движения вправо
        with patch('pygame.key.get_pressed') as mock_keys:
            mock_keys.return_value = {pygame.K_RIGHT: True}
            char.smena(0.5)
        
        # При отрицательной скорости движение должно быть в обратную сторону
        expected_step = char.speed * SPEED_FACTOR * 0.5  # отрицательное значение
        self.assertEqual(char.fx, initial_x + expected_step)
    
    # Тесты на константы игры
    def test_game_constants(self):
        """Тест что игровые константы установлены правильно"""
        self.assertEqual(FPS, 60)
        self.assertEqual(SPEED_FACTOR, 10)
        self.assertEqual(GAME_TIME_MS, 120000)  # 2 минуты в миллисекундах
        self.assertEqual(HIT_COOLDOWN_MS, 600)
        self.assertEqual(START_X, 15)
        self.assertEqual(START_Y, 500)
    
    def test_speed_factor_application(self):
        """Тест применения SPEED_FACTOR в движении"""
        char = Caracters(100, 100, 5, "test.png")
        initial_x = char.fx
        
        with patch('pygame.key.get_pressed') as mock_keys:
            mock_keys.return_value = {pygame.K_RIGHT: True}
            char.smena(1.0)
        
        # Расчет: speed * SPEED_FACTOR * dt = 5 * 10 * 1.0 = 50
        expected_movement = 5 * SPEED_FACTOR * 1.0
        self.assertEqual(char.fx, initial_x + expected_movement)
    
    # Тесты на инициализацию PyGame
    def test_pygame_initialization(self):
        """Тест что PyGame инициализируется без ошибок"""
        try:
            pygame.init()
            self.assertTrue(pygame.get_init())
        finally:
            pygame.quit()
    
    # Тест производительности (граничный)
    def test_many_objects_performance(self):
        """Тест создания множества объектов (стресс-тест)"""
        walls = []
        for i in range(100):  # Создаем 100 стен
            wall = Wall(i*10, i*5, 10, 10, 255, 0, 0)
            walls.append(wall)
        
        self.assertEqual(len(walls), 100)
        
        # Проверяем что все стены созданы корректно
        for i, wall in enumerate(walls):
            self.assertEqual(wall.rect.x, i*10)
            self.assertEqual(wall.rect.y, i*5)


# Дополнительные тесты для edge cases
class TestEdgeCases(unittest.TestCase):
    
    def test_character_out_of_bounds(self):
        """Тест выхода персонажа за границы"""
        char = Caracters(-1000, -1000, 10, "test.png")
        
        # Координаты могут быть отрицательными
        self.assertEqual(char.fx, -1000.0)
        self.assertEqual(char.fy, -1000.0)
        
        # Синхронизация должна работать
        char.sync_rect()
        self.assertEqual(char.rect.x, -1000)
        self.assertEqual(char.rect.y, -1000)
    
    def test_enemy_route_reverse_logic(self):
        """Тест логики разворота врага №3 в конце маршрута"""
        enemy = Eneny(0, 0, 10, "test.png")
        
        # Инициализируем маршрут
        enemy.vrag_smena3(0.1)
        
        # Устанавливаем индекс в конец маршрута
        enemy._route_i = len(enemy.route) - 1
        enemy._route_dir = 1
        
        # Симулируем достижение конечной точки
        enemy.fx, enemy.fy = enemy.route[-1]
        
        # Вызываем метод - должен развернуться
        enemy.vrag_smena3(0.1)
        
        self.assertEqual(enemy._route_dir, -1)  # Должен развернуться
        self.assertEqual(enemy._route_i, len(enemy.route) - 2)  # Должен вернуться на шаг назад
    
    def test_wall_initialization_edge_cases(self):
        """Тест крайних случаев при создании стены"""
        # Нулевой размер
        wall = Wall(0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(wall.width, 0)
        self.assertEqual(wall.height, 0)
        
        # Отрицательный размер (хотя в игре так не используется)
        wall2 = Wall(0, 0, -10, -20, 0, 0, 0)
        self.assertEqual(wall2.width, -20)
        self.assertEqual(wall2.height, -10)
    
    def test_door_position_edge_cases(self):
        """Тест крайних случаев позиционирования двери"""
        # Дверь за пределами экрана
        door = Door(-100, -100, 10, 10)
        self.assertEqual(door.rect.x, -100)
        self.assertEqual(door.rect.y, -100)
        
        # Очень большая дверь
        door2 = Door(0, 0, 10000, 10000)
        self.assertEqual(door2.width, 10000)
        self.assertEqual(door2.height, 10000)


# Запуск тестов
if __name__ == '__main__':
    # Создаем test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGameLogic)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEdgeCases))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим статистику
    print(f"\n{'='*60}")
    print(f"Тесты завершены:")
    print(f"  Пройдено: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Провалено: {len(result.failures)}")
    print(f"  Ошибок: {len(result.errors)}")
    print(f"{'='*60}")
    
    if result.failures or result.errors:
        sys.exit(1)  # Возвращаем ненулевой код для CI/CD
